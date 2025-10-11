
    // Edit session name and description
    function editSessionName(sessionId) {
        const sessionItem = document.querySelector(`[data-session-id="${sessionId}"]`);
        const nameElement = sessionItem.querySelector('.session-name');
        const descElement = sessionItem.querySelector('.session-description');

        const currentName = nameElement.textContent.trim();
        const currentDesc = descElement.textContent.trim();

        // Prompt for new values
        const newName = prompt('Enter new session name:', currentName);
        if (newName === null) return; // Cancelled

        if (!newName.trim()) {
            alert('Session name cannot be empty');
            return;
        }

        const newDesc = prompt('Enter new description (optional):', currentDesc);
        if (newDesc === null) return; // Cancelled

        // Send update request
        const formData = new FormData();
        formData.append('name', newName.trim());
        formData.append('description', newDesc.trim());

        fetch(`/rf-analyzer/session/update/${sessionId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update UI
                nameElement.textContent = data.name;
                descElement.textContent = data.description;

                // Update data attributes for sorting
                sessionItem.setAttribute('data-name', data.name.toLowerCase());

                // Show success message
                alert('Session updated successfully!');
            } else {
                alert('Failed to update session: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update session');
        });
    }
