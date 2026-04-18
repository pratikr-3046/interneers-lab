const container = document.getElementById('product-container');

fetch('http://127.0.0.1:8000/api/products/')
    .then(res => res.json())
    .then(data => {
        container.innerHTML = '';
        
        data.forEach(product => {
            const tile = document.createElement('div');
            tile.className = 'product-tile';
            
            tile.innerHTML = `
                <h2 class="title">${product.name}</h2>
                <p class="description">Brand: ${product.brand}</p>
                <div class="price">$${product.price}</div>
            `;
            
            container.appendChild(tile);
        });
    });