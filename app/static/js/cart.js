//Clave para el LocalStorage
const CART_KEY = 'keepklothing_cart';

//Creamos la clase de carrito
const Cart = {
    //Recuperar el carrito
    getCart: function () {
        const cart = localStorage.getItem(CART_KEY);
        return cart ? JSON.parse(cart) : [];
    },

    //Guardar el carrito
    saveCart: function (cart) {
        localStorage.setItem(CART_KEY, JSON.stringify(cart));
        this.updateCartCount();
    },

    //Añadir producto al carrito
    add: function (product) {
        let cart = this.getCart();
        const existingProductIndex = cart.findIndex(item => item.id === product.id);

        if (existingProductIndex > -1) {
            cart[existingProductIndex].quantity += 1;
        } else {
            product.quantity = 1;
            cart.push(product);
        }

        this.saveCart(cart);
        alert('Producto añadido al carrito');
    },

    //Eliminar un producto del carrito
    remove: function (productId) {
        let cart = this.getCart();
        cart = cart.filter(item => item.id !== productId);
        this.saveCart(cart);
        this.renderCartPage();
    },

    //Modificar Cantidad del carrito
    updateQuantity: function (productId, quantity) {
        let cart = this.getCart();
        const productIndex = cart.findIndex(item => item.id === productId);

        if (productIndex > -1) {
            if (quantity <= 0) {
                this.remove(productId);
            } else {
                cart[productIndex].quantity = parseInt(quantity);
                this.saveCart(cart);
                this.renderCartPage();
            }
        }
    },

    //Vaciar el carrito
    clear: function () {
        localStorage.removeItem(CART_KEY);
        this.updateCartCount();
        this.renderCartPage();
    },

    //Log consola
    updateCartCount: function () {
        const cart = this.getCart();
        const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
        console.log('Cart count updated:', totalCount);
    },

    //Calcular valor total
    calculateTotal: function () {
        const cart = this.getCart();
        return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2);
    },

    //Renderizar página carrito
    renderCartPage: function () {
        const cartContainer = document.getElementById('cart-items-container');
        const cartSubTotalElement = document.getElementById('cart-subtotal');
        const cartTotalElement = document.getElementById('cart-total');

        if (!cartContainer) return;

        const cart = this.getCart();
        cartContainer.innerHTML = '';

        if (cart.length === 0) {
            cartContainer.innerHTML = '<p>Tu carrito está vacío.</p>';
            if (cartSubTotalElement) cartSubTotalElement.innerText = '0.00 €';
            if (cartTotalElement) cartTotalElement.innerText = '0.00 €';

            return;
        }

        cart.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.classList.add('cart-item');
            itemElement.innerHTML = `
                <div class="item-image">
                    <img src="${item.image}" alt="${item.name}" style="width: 80px; height: 80px; object-fit: cover;">
                </div>
                <div class="item-details">
                    <h4>${item.name}</h4>
                    <p class="price">${item.price} €</p>
                </div>
                <div class="item-actions">
                    <input type="number" min="1" value="${item.quantity}" onchange="Cart.updateQuantity(${item.id}, this.value)">
                    <button id="delete-btn" onclick="Cart.remove(${item.id})">Eliminar</button>
                </div>
            `;
            cartContainer.appendChild(itemElement);
        });

        if (cartSubTotalElement) {
            cartSubTotalElement.innerText = this.calculateTotal() + ' €';
        }

        if (cartTotalElement) {
            cartTotalElement.innerText = this.calculateTotal() + ' €';
        }
    },

    //Tramitar pedido hacer, fetch a la API
    checkout: function () {
        const cart = this.getCart();
        if (cart.length === 0) {
            alert('Tu carrito está vacío');
            return;
        }

        if (!confirm('¿Estás seguro de que quieres tramitar el pedido?')) {
            return;
        }
        //Fetch a la API
        fetch('/api/tramitar-pedido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '',
            },
            body: JSON.stringify({ cart: cart })
        })
            .then(response => {
                if (response.status === 401) {
                    return response.json().then(data => {
                        throw { type: 'auth_error', message: data.message };
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    this.clear();
                    window.location.href = '/';
                } else {    //No autenticado
                    if (data.error_code === 'not_authenticated') {
                        alert(data.message);
                        window.location.href = '/login/';
                    } else {
                        alert('Error: ' + data.message);
                    }
                }
            })
            //error en el auth
            .catch(error => {
                if (error.type === 'auth_error') {
                    alert(error.message);
                    window.location.href = '/login/';
                } else {
                    console.error('Error:', error);
                    alert('Hubo un error al procesar el pedido.');
                }
            });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Cart.updateCartCount();
    Cart.renderCartPage();
});
