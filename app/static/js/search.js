document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const suggestionsContainer = document.getElementById('search-suggestions');

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value;

            if (query.length === 0) {
                suggestionsContainer.innerHTML = '';
                suggestionsContainer.style.display = 'none';
                return;
            }

            fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsContainer.innerHTML = '';
                    if (data.results.length > 0) {
                        suggestionsContainer.style.display = 'block';
                        data.results.forEach(product => {
                            const div = document.createElement('div');
                            div.classList.add('suggestion-item');
                            div.innerHTML = `
                                <div class="suggestion-content">
                                    <img src="/static${product.imagen_url}" alt="Producto" class="suggestion-image">
                                    <div class="suggestion-details">
                                        <span class="suggestion-name">${product.nombre}</span>
                                        <span class="suggestion-price">${product.precio}€</span>
                                    </div>
                                </div>
                            `;
                            div.addEventListener('click', function () {
                                window.location.href = `/productos/${product.id}/`;
                            });
                            suggestionsContainer.appendChild(div);
                        });
                    } else {
                        suggestionsContainer.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error fetching suggestions:', error);
                });
        });

        // Close suggestions when clicking outside
        document.addEventListener('click', function (event) {
            const searchBar = document.getElementById('searchBar');
            if (searchBar && !searchBar.contains(event.target)) {
                suggestionsContainer.style.display = 'none';
            }
        });
    }
});
