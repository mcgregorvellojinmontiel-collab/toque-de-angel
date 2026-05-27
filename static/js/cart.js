function formatPrice(value) {
    return Number(value).toLocaleString('es-CO', {
        maximumFractionDigits: 0
    });
}

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

    alert(name + ' Se añadio al carrito!');
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
                        $${formatPrice(product.price * product.quantity)}
                    </strong>

                </div>

            </div>

        `;
    });

    cartTotal.innerText = `Total: $${formatPrice(total)}`;
}


function sendWhatsAppOrder() {

    const cart = getCart();

    if (cart.length === 0) {
        alert('El carrito está vacío. Agrega productos antes de hacer el pedido.');
        return;
    }

    const customerName = prompt('Escribe tu nombre:');

    if (!customerName || customerName.trim() === '') {
        alert('Debes escribir tu nombre para continuar.');
        return;
    }

    const customerAddress = prompt('Escribe tu dirección de entrega:');

    if (!customerAddress || customerAddress.trim() === '') {
        alert('Debes escribir la dirección de entrega.');
        return;
    }

    const notes = prompt('Observaciones del pedido, ejemplo: sin azúcar, para recoger, etc. Si no tienes, puedes dejarlo vacío.');

    let total = 0;

    let message = 'Hola, quiero realizar el siguiente pedido:%0A%0A';

    message += 'Datos del cliente:%0A';
    message += `Nombre: ${customerName}%0A`;
    message += `Dirección: ${customerAddress}%0A`;

    if (notes && notes.trim() !== '') {
        message += `Observaciones: ${notes}%0A`;
    }

    message += '%0AProductos:%0A';

    cart.forEach(product => {

        const subtotal = product.price * product.quantity;

        total += subtotal;

        message += `- ${product.name} x${product.quantity} - $${formatPrice(subtotal)}%0A`;
    });

    message += `%0ATotal del pedido: $${formatPrice(total)}%0A%0A`;
    message += 'Quedo atento a la confirmación.';

    const phone = '573053521301';

    window.open(
        `https://wa.me/${phone}?text=${message}`,
        '_blank'
    );
}

function searchProducts() {

    const input = document.getElementById('productSearch');

    if (!input) {
        return;
    }

    const searchText = input.value.toLowerCase();

    const products = document.querySelectorAll('.searchable-product');

    products.forEach(product => {

        const productName = product.querySelector('h2').innerText.toLowerCase();

        if (productName.includes(searchText)) {
            product.style.display = 'flex';
        } else {
            product.style.display = 'none';
        }
    });
}


renderCart();
