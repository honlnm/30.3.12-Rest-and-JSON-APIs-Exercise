function generateCupcakeHTML(cupcake) {
    return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor} / ${cupcake.size}
        </li>
        <img class="Cupcake-img"
              src="${cupcake.image}"
              alt="(no image provided)">
      </div>
    `;
}

async function showInitialCupcakes() {
    const response = await axios.get(`/api/cupcakes`);

    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $("ul").append(newCupcake);
    }
}

$("form").on("submit", async function (evt) {
    evt.preventDefault();

    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    const newCupcakeResponse = await axios.post(`/api/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("ul").append(newCupcake);
    $("form").trigger("reset");
});

$(showInitialCupcakes)