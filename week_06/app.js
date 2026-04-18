const container = document.getElementById('product-container');

fetch('http://127.0.0.1:8000/api/products/')
    .then(res => res.json())
    .then(data => {
        container.innerHTML = '';

        data.forEach(product => {
            const tile = document.createElement('div');
            tile.className = 'product-tile';

            const title = document.createElement('h2');
            title.className = 'title';
            title.textContent = product.name; 

            const brand = document.createElement('p');
            brand.className = 'description';
            brand.textContent = `Brand: ${product.brand}`;

            const price = document.createElement('div');
            price.className = 'price';
            price.textContent = `$${product.price}`;

            tile.appendChild(title);
            tile.appendChild(brand);
            tile.appendChild(price);
            
            container.appendChild(tile);
        });
    })
    .catch(err => console.error("Fetch error:", err));