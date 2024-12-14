function filterLands() {
  const acres = document.getElementById('acres').value;

  $.ajax({
      url: '/filter_lands',
      type: 'GET',
      data: {
          acres: acres,
      },
      success: function(response) {
          const landContainer = document.querySelector('.main-land-container');
          landContainer.innerHTML = '';  // Clear current land display

          response.lands.forEach(function(land) {
              const landElement = document.createElement('div');
              landElement.classList.add('land-container');

              landElement.innerHTML = `
                  <div class="land-name">
                      <div class="land15">${land.lname}</div>
                  </div>
                  <div class="product-details-container">
                      <div class="land-image">
                          ${land.cover_image ? `<img src="data:image/jpeg;base64,${land.cover_image}" alt="${land.lname}">` : '<img src="https://via.placeholder.com/300" alt="No Image">'}
                      </div>
                      <div class="abstract-details-container">
                          <div class="data" id="data1">
                              <div>
                                  <p>Acres</p>
                                  <p class="no-of-acres">${land.acres}</p>
                              </div>
                              <div>
                                  <p>Location</p>
                                  <p>${land.location}</p>
                              </div>
                          </div>
                          <div class="data">
                              <div>
                                  <p>Water</p>
                                  <p>${land.watersource ? 'Yes' : 'No'}</p>
                              </div>
                              <div>
                                  <p>Soil Type</p>
                                  <p>${land.soil}</p>
                              </div>
                          </div>
                          <a class="view_more" href="/land_info/${land.id}">View More...</a>
                      </div>
                  </div>
              `;
              landContainer.appendChild(landElement);
          });
      },
      error: function(error) {
          console.error('Error:', error);
      }
  });
}
