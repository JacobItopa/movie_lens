const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadSection = document.getElementById('upload-section');
const loadingSection = document.getElementById('loading-section');
const resultSection = document.getElementById('result-section');
const errorSection = document.getElementById('error-section');
const loadingText = document.getElementById('loading-text');

// Drag & Drop Handlers
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleFiles(e.dataTransfer.files);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFiles(e.target.files);
    }
});

// Main Logic
async function handleFiles(files) {
    if (files.length === 0) return;

    // UI State -> Loading
    uploadSection.classList.add('hidden');
    resultSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');

    // Simulate steps text
    const fileCount = files.length;
    loadingText.textContent = `Analyzing ${fileCount} screenshot${fileCount > 1 ? 's' : ''}...`;

    setTimeout(() => { if (!loadingSection.classList.contains('hidden')) loadingText.textContent = "Connecting the dots..." }, 1500);
    setTimeout(() => { if (!loadingSection.classList.contains('hidden')) loadingText.textContent = "Searching for streaming links..." }, 3500);

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        if (files[i].type.startsWith('image/')) {
            // Use 'images' key and include filename
            formData.append('images', files[i], files[i].name);
        }
    }

    try {
        const response = await fetch('/api/identify', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Failed to process images");
        }

        if (result.success) {
            showResult(result.data);
        } else {
            showError("We couldn't identify a movie. Try clearer screenshots!");
        }

    } catch (error) {
        console.error(error);
        showError("Something went wrong on our end. Please try again.");
    } finally {
        loadingSection.classList.add('hidden');
        loadingText.textContent = "Analyzing Scene...";
    }
}

function showResult(data) {
    resultSection.classList.remove('hidden');

    // Populate data
    document.getElementById('movie-title').textContent = data.title;
    document.getElementById('movie-year').textContent = data.year || 'Unknown Year';
    document.getElementById('movie-summary').textContent = data.summary;

    // Confidence
    const confidencePercent = Math.round((data.confidence || 0) * 100);
    document.getElementById('confidence-badge').innerHTML = `<i class="fa-solid fa-check-circle"></i> ${confidencePercent}% Match`;

    // Links
    const linksGrid = document.getElementById('links-grid');
    linksGrid.innerHTML = '';

    if (data.links && data.links.length > 0) {
        data.links.forEach(link => {
            const domain = new URL(link.url).hostname.replace('www.', '');
            const a = document.createElement('a');
            a.className = 'link-item';
            a.href = link.url;
            a.target = '_blank';
            a.innerHTML = `
                <span>Watch on <strong>${domain}</strong></span>
                <i class="fa-solid fa-external-link-alt"></i>
            `;
            linksGrid.appendChild(a);
        });
    } else {
        linksGrid.innerHTML = '<div style="color:var(--text-secondary)">No specific streaming links found.</div>';
    }
}

function showError(message) {
    loadingSection.classList.add('hidden');
    errorSection.classList.remove('hidden');
    document.getElementById('error-message').textContent = message;
}

// Reset Handlers
document.getElementById('close-btn').addEventListener('click', resetUI);
document.getElementById('retry-btn').addEventListener('click', resetUI);

function resetUI() {
    resultSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    uploadSection.classList.remove('hidden');
    fileInput.value = ''; // Reset input
}
