document.getElementById('searchForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const productId = document.getElementById('productId').value.trim();
    const resultDiv = document.getElementById('result');

    resultDiv.innerHTML = '<p>Searching...</p>';

    try {
        const response = await fetch(`http://127.0.0.1:8000/search-product/?q=${encodeURIComponent(productId)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayResult(data.response.data);
        } else {
            const errorText = await response.text();
            resultDiv.innerHTML = `<p>Error: ${response.status} - ${errorText}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});

function displayResult(data) {
    if (!data || data.length === 0) {
        document.getElementById('result').innerHTML = '<p>No results found</p>';
        return;
    }

    const table = `
        <table>
            <thead>
                <tr>
                    <th>Product ID</th>
                    <th>Pricing Logic</th>
                    <th>Product Family</th>
                    <th>Product Line</th>
                    <th>List Label</th>
                    <th>Product Group</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(item => `
                    <tr>
                        <td>${item.sku || ''}</td>
                        <td></td>
                        <td>${item.label || ''}</td>
                        <td>${item.listId || ''}</td>
                        <td>${item.listLabel || ''}</td>
                        <td>${item.productGroup || ''}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    document.getElementById('result').innerHTML = table;
}
