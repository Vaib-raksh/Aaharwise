const API_BASE = 'http://127.0.0.1:8000';
let selectedFood = '';
let latestNutrition = null;
const searchForm = document.querySelector('#search-form');
const nutritionForm = document.querySelector('#nutrition-form');
const searchResults = document.querySelector('#search-results');
const nutritionResult = document.querySelector('#nutrition-result');

searchForm.addEventListener('submit', async (event) => { event.preventDefault(); await searchFoods(new FormData(searchForm).get('query')); });
document.querySelectorAll('[data-query]').forEach((button) => button.addEventListener('click', () => { document.querySelector('#food-query').value = button.dataset.query; searchFoods(button.dataset.query); }));

async function searchFoods(query) {
  searchResults.innerHTML = '<p class="muted">Reading the food atlas...</p>';
  try {
    const response = await fetch(`${API_BASE}/api/foods/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error('Catalog search failed.');
    const data = await response.json();
    searchResults.innerHTML = data.foods.length ? data.foods.slice(0, 5).map((food) => `<button class="food-option" type="button" data-food="${food.food_name}"><b>${food.food_name}</b><span>${food.food_group || 'IFCT food'} ↗</span></button>`).join('') : '<p class="muted">No matching IFCT foods found.</p>';
    document.querySelectorAll('.food-option').forEach((button) => button.addEventListener('click', () => selectFood(button.dataset.food)));
  } catch (error) { searchResults.innerHTML = `<p class="muted">${error.message} Is the API running?</p>`; }
}

function selectFood(food) {
  selectedFood = food;
  document.querySelector('#selected-food').textContent = food;
  document.querySelector('#selected-source').textContent = 'IFCT / 2017';
  document.querySelector('.plate-panel').scrollIntoView({ behavior: 'smooth', block: 'center' });
  loadNutrition();
}
nutritionForm.addEventListener('submit', (event) => { event.preventDefault(); loadNutrition(); });

async function loadNutrition() {
  if (!selectedFood) return;
  const quantity = document.querySelector('#quantity').value;
  nutritionResult.innerHTML = '<p class="muted">Calculating your nutritional fingerprint...</p>';
  const response = await fetch(`${API_BASE}/api/nutrition?food=${encodeURIComponent(selectedFood)}&quantity_g=${quantity}`);
  if (!response.ok) { nutritionResult.innerHTML = '<p class="muted">Nutrition data could not be loaded.</p>'; return; }
  latestNutrition = await response.json();
  const metrics = [['Energy', latestNutrition.energy_kj, 'kJ', 'energy'], ['Protein', latestNutrition.protein_g, 'g', ''], ['Carbs', latestNutrition.carbohydrate_g, 'g', ''], ['Fat', latestNutrition.fat_g, 'g', ''], ['Fiber', latestNutrition.fiber_g, 'g', '']];
  nutritionResult.innerHTML = `<div class="nutrition-grid">${metrics.map(([label, value, unit, extra]) => `<div class="metric ${extra}"><span>${label}</span><strong>${Number(value).toFixed(1)} ${unit}</strong></div>`).join('')}</div>`;
  updateInsights();
}

function updateInsights() {
  const protein = Number(latestNutrition.protein_g) || 0;
  const fiber = Number(latestNutrition.fiber_g) || 0;
  const carbs = Number(latestNutrition.carbohydrate_g) || 0;
  const score = Math.min(96, Math.round(35 + protein * 3 + fiber * 5));
  document.querySelector('#pulse-score').textContent = score;
  document.querySelector('#pulse-bar').style.width = `${score}%`;
  document.querySelector('#pulse-copy').textContent = score > 65 ? 'A nourishing signal, with room for the rest of the plate.' : 'A useful start. Balance this with protein, fiber, and color.';
  const bars = [['Protein', protein, Math.min(100, protein * 6), 'protein'], ['Carbs', carbs, Math.min(100, carbs), 'carbs'], ['Fiber', fiber, Math.min(100, fiber * 18), 'fiber']];
  document.querySelector('#macro-bars').innerHTML = bars.map(([label, value, width, type]) => `<div class="macro-row"><span>${label}</span><div class="bar-track"><span class="bar-fill ${type}" style="width:${width}%"></span></div><b>${value.toFixed(1)}g</b></div>`).join('');
  document.querySelector('#meaning-title').textContent = fiber >= 4 ? 'A little more staying power.' : 'A bright start, not the whole story.';
  document.querySelector('#meaning-copy').textContent = fiber >= 4 ? 'Fiber helps this meal feel more complete. Keep building variety across the day.' : 'This food brings energy. Pair it with a fiber-rich side to widen the signal.';
}

document.querySelector('#timeline-button').addEventListener('click', async () => {
  const timeline = document.querySelector('#timeline');
  timeline.innerHTML = '<p class="muted">Opening your longer view...</p>';
  const protein = latestNutrition?.protein_g || 0;
  const fiber = latestNutrition?.fiber_g || 0;
  const response = await fetch(`${API_BASE}/api/timeline?protein_g=${protein}&fiber_g=${fiber}`);
  const data = await response.json();
  timeline.innerHTML = data.timeline.map((item, index) => `<article class="timeline-card" style="animation-delay:${index * 70}ms"><span class="horizon-mark">${index === 0 ? '●' : '○'}</span><div><span class="horizon-time">${item.stage}</span><h3>${item.mechanism}</h3><p>${item.implication}</p></div></article>`).join('');
  timeline.scrollIntoView({ behavior: 'smooth', block: 'start' });
});