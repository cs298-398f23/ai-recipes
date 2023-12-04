// JavaScript (app.js)
const resultsContainer = document.getElementById('resultsContainer');
const prevPageButton = document.getElementById('prevPage');
const nextPageButton = document.getElementById('nextPage');
const currentPageSpan = document.getElementById('currentPage');
let currentPage = 1; // Initialize current page to 1
let searchQuery = ''; // Initialize searchQuery

// Function to fetch search results based on page number
function fetchSearchResults(page) {
    // Encode the search query to ensure it's safe for a URL
    const encodedQuery = encodeURIComponent(searchQuery);
    fetch(`http://127.0.0.1:5000/search?page=${page}&query=${encodedQuery}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Call the displaySearchResults function to handle and display the results
        displaySearchResults(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function displaySearchResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = '';  // Clear previous results

    if (data.success) {
        // Loop through the received recipes and append them to the container
        data.data.forEach(recipe => {
            const recipeDiv = document.createElement('div');

            // Ensure the link is an absolute URL
            const absoluteLink = recipe.link.startsWith('http') ? recipe.link : `http://${recipe.link}`;

            recipeDiv.innerHTML = `
                <h3>${removeQuotes(recipe.title)}</h3>
                <p>${removeQuotes(recipe.NER)}</p>
                <p><a href="${absoluteLink}" target="_blank">${recipe.link}</a></p>
            `;
            resultsContainer.appendChild(recipeDiv);
        });
    } else {
        // Display an error message
        const errorDiv = document.createElement('div');
        errorDiv.textContent = `Error: ${data.message}`;
        resultsContainer.appendChild(errorDiv);
    }
}


// Function to update pagination controls
function updatePaginationControls() {
    document.getElementById('currentPage').textContent = `Page ${currentPage}`;
}

// Event listeners for previous and next buttons
prevPageButton.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchSearchResults(currentPage);
        updatePaginationControls();
    }
});

nextPageButton.addEventListener('click', () => {
    currentPage++;
    fetchSearchResults(currentPage);
    updatePaginationControls();
});

// Helper function to remove double quotes from a string
function removeQuotes(str) {
    return str.replace(/"/g, '');
}

// Event listener for the search form
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    searchQuery = document.getElementById('searchInput').value;
    currentPage = 1; // Reset to the first page when a new search is performed
    fetchSearchResults(currentPage);
    updatePaginationControls();
});

