document.addEventListener("DOMContentLoaded", () => {
    const products = document.querySelectorAll(".product");

    // Handle rating stars
    products.forEach((product) => {
        const stars = product.querySelectorAll(".star");
        const ratingDisplay = product.querySelector(".rating-value span");
        let currentRating = 0;

        stars.forEach((star, index) => {
            star.addEventListener("mouseover", () => {
                highlightStars(index, stars);
            });

            star.addEventListener("mouseout", () => {
                resetStars(stars, currentRating);
            });

            star.addEventListener("click", () => {
                setRating(index + 1, stars, ratingDisplay);
            });
        });

        function highlightStars(index, stars) {
            stars.forEach((star, i) => {
                star.classList.toggle("hovered", i <= index);
            });
        }

        function resetStars(stars, rating) {
            stars.forEach((star, i) => {
                star.classList.toggle("hovered", false);
                star.classList.toggle("selected", i < rating);
            });
        }

        function setRating(rating, stars, ratingDisplay) {
            currentRating = rating;
            ratingDisplay.textContent = currentRating;
            stars.forEach((star, i) => {
                star.classList.toggle("selected", i < currentRating);
            });
        }
    });

    // Handle "Add to Wishlist" button
    document.querySelectorAll('.add-to-wishlist').forEach((button) => {
        button.addEventListener('click', () => {
            const productId = button.dataset.productId;

            // Send request to add product to wishlist
            fetch(`/add_to_wishlist/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_id: productId }),
            })
            .then(response => response.json())
            .then(data => {
                // Update button text and disable it after adding to wishlist
                button.textContent = "Added to Wishlist";
                button.style.backgroundColor = "#ccc";
                button.style.cursor = "not-allowed";
                button.disabled = true;
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Something went wrong. Please try again later.');
            });
        });
    });
});
