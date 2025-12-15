const CART_KEY = 'keepklothing_cart';

const Cart = {
    getCart: function () {
        const cart = localStorage.getItem(CART_KEY);
        return cart ? JSON.parse(cart) : [];
    },

    saveCart: function (cart) {
        localStorage.setItem(CART_KEY, JSON.stringify(cart));
        this.updateCartCount();
    },

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

    remove: function (productId) {
        let cart = this.getCart();
        cart = cart.filter(item => item.id !== productId);
        this.saveCart(cart);
        this.renderCartPage();
    },

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

    clear: function () {
        localStorage.removeItem(CART_KEY);
        this.updateCartCount();
        this.renderCartPage();
    },

    updateCartCount: function () {
        const cart = this.getCart();
        const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
        console.log('Cart count updated:', totalCount);
    },

    calculateTotal: function () {
        const cart = this.getCart();
        return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2);
    },

    renderCartPage: function () {
        const cartContainer = document.getElementById('cart-items-container');
        const cartTotalElement = document.getElementById('cart-total');

        if (!cartContainer) return;

        const cart = this.getCart();
        cartContainer.innerHTML = '';

        if (cart.length === 0) {
            cartContainer.innerHTML = '<p>Tu carrito está vacío.</p>';
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
                    <button onclick="Cart.remove(${item.id})">Eliminar</button>
                    <p class="subtotal">Total: ${(item.price * item.quantity).toFixed(2)} €</p>
                </div>
            `;
            cartContainer.appendChild(itemElement);
        });

        if (cartTotalElement) {
            cartTotalElement.innerText = this.calculateTotal() + ' €';
        }
    },

    checkout: function () {
        const cart = this.getCart();
        if (cart.length === 0) {
            alert('Tu carrito está vacío');
            return;
        }

        if (!confirm('¿Estás seguro de que quieres tramitar el pedido?')) {
            return;
        }

        fetch('/api/tramitar-pedido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ cart: cart })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    this.clear();
                    window.location.href = '/';
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error al procesar el pedido.');
            });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Cart.updateCartCount();
    Cart.renderCartPage();
});
