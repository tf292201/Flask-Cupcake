const BASE_URL = 'http://localhost:5000';

function generateCupcake(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <img class="Cupcake-img" src="${cupcake.image}">
      </li>
      <button class="delete-button">X</button>
    </div>
  `;
}

async function showCupcakes() {
  const response = await axios.get(`${BASE_URL}/api/cupcakes`);
  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(generateCupcake(cupcakeData));
    $('#cupcakes-list').append(newCupcake);
  }
}

$(document).ready(function() {
  showCupcakes();
});

$('#new-cupcake-form').on('submit', async function (evt) {
  evt.preventDefault();

  let flavor = $('#form-flavor').val();
  let size = $('#form-size').val();
  let rating = $('#form-rating').val();
  let image = $('#form-image').val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/api/cupcakes`, {
    flavor,
    size,
    rating,
    image
  });

  let newCupcake = $(generateCupcake(newCupcakeResponse.data.cupcake));
  $('#cupcakes-list').append(newCupcake);
  $('#new-cupcake-form').trigger('reset');
});

$('#cupcakes-list').on('click', '.delete-button', async function (evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest('div');
  let cupcakeId = $cupcake.attr('data-cupcake-id');

  await axios.delete(`${BASE_URL}/api/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

