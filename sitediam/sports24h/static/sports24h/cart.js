document.addEventListener('DOMContentLoaded', () => {
    const decreaseButtons = document.querySelectorAll('.decrease-quantity');
    const increaseButtons = document.querySelectorAll('.increase-quantity');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const totalAmount = document.getElementById('total-amount');

    // Event listener for decrease buttons
    decreaseButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            const productId = event.target.dataset.productId;
            const input = document.querySelector(`.quantity-input[data-product-id="${productId}"]`);
            const currentValue = parseInt(input.value);
            if (currentValue > 1) {
                input.value = currentValue - 1;
                updateTotalAmount();
            }
        });
    });

    // Event listener for increase buttons
    increaseButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            const productId = event.target.dataset.productId;
            const input = document.querySelector(`.quantity-input[data-product-id="${productId}"]`);
            const currentValue = parseInt(input.value);
            input.value = currentValue + 1;
            updateTotalAmount();
        });
    });

    // Event listener for quantity inputs
    quantityInputs.forEach((input) => {
        input.addEventListener('change', () => {
            updateTotalAmount();
        });
    });

    // Function to update the total amount
    function updateTotalAmount() {
        let total = 0;
        document.querySelectorAll('.cart-item').forEach((item) => {
            const price = parseFloat(item.querySelector('.price').textContent.replace('$', ''));
            const quantity = parseInt(item.querySelector('.quantity-input').value);
            const subtotal = price * quantity;
            total += subtotal;
        });
        totalAmount.textContent = '$' + total.toFixed(2);
    }
});