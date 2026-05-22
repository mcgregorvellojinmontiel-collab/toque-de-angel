function addToCart(id, name, price, image) {

    let cart = JSON.parse(
        localStorage.getItem('cart')
    ) || [];

    const existingProduct = cart.find(
        item => item.id === id
    );

    if (existingProduct) {

        existingProduct.quantity += 1;

    } else {

        cart.push({
            id,
            name,
            price,
            image,
            quantity: 1
        });
    }

    localStorage.setItem(
        'cart',
        JSON.stringify(cart)
    );

    renderCart();

    alert(name + ' added to cart!');
}


function getCart() {

    return JSON.parse(
        localStorage.getItem('cart')
    ) || [];
}


function clearCart() {

    localStorage.removeItem('cart');

    renderCart();
}


function toggleCart() {

    const sidebar = document.getElementById(
        'cart-sidebar'
    );

    sidebar.classList.toggle('active');
}


function renderCart() {

    const cart = getCart();

    const cartItems = document.getElementById(
        'cart-items'
    );

    const cartTotal = document.getElementById(
        'cart-total'
    );

    cartItems.innerHTML = '';

    let total = 0;

    cart.forEach(product => {

        total += product.price * product.quantity;

        cartItems.innerHTML += `

            <div class="cart-item">

                <img src="${product.image}">

                <div>

                    <h4>${product.name}</h4>

                    <p>
                        Qty: ${product.quantity}
                    </p>

                    <strong>
                        $${product.price}
                    </strong>

                </div>

            </div>

        `;
    });

    cartTotal.innerText = `Total: $${total}`;
}


function sendWhatsAppOrder() {

    const cart = getCart();

    if (cart.length === 0) {

        alert('Cart is empty');

        return;
    }

    let message = 'Buenas, quiero hacer un pedido de:%0A%0A';

    let total = 0;

    cart.forEach(product => {

        total += product.price * product.quantity;

        message += `${product.name} x${product.quantity} - $${product.price * product.quantity}%0A`;
    });

    message += `%0A Total: $${total}`;

    const phone = '3053521301';

    window.open(
        `https://wa.me/${phone}?text=${message}`,
        '_blank'
    );
}


renderCart();
