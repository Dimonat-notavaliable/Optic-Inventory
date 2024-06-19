function getQueryParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}


function loadSchemeList(schemeSelector){
    // Загрузка списка схем
    fetch(`all/`)
        .then(response => response.json())
        .then(data => {
            data.schemes.forEach(scheme => {
                const option = document.createElement('option');
                option.value = scheme.id;
                option.text = `Схема от ${scheme.last_change}`;
                schemeSelector.appendChild(option);
            });
            // Устанавливаем выбранную схему
            const selectedSchemeId = getQueryParameter('scheme_id');
            if (selectedSchemeId) {
                schemeSelector.value = selectedSchemeId;
            } else {
                // Устанавливаем последнюю схему как выбранную, если параметр не указан
                const lastScheme = data.schemes[0];
                if (lastScheme) {
                    schemeSelector.value = lastScheme.id;
                }
            }
        })
        .catch(error => console.error('Ошибка при загрузке списка схем:', error));
}