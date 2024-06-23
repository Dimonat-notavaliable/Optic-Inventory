function getQueryParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}


function loadSchemeList(schemeSelector){
    schemeSelector.innerHTML = '<option value="" disabled>Выберите схему</option>';

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

// JavaScript: функции для отображения и закрытия модального окна
function showModal(header, message) {
    const modal = document.getElementById('statusModal');

    const modalMessage = document.getElementById('modalMessage');
    modalMessage.textContent = message;

    const modalHeader = document.getElementById('modalHeader');
    modalHeader.textContent = header;

    modal.style.display = 'block';
    document.body.classList.add('no-scroll'); // Disable scroll

    const closeModal = document.getElementById('closeModal');
    closeModal.onclick = function() {
        modal.style.display = 'none';
        document.body.classList.remove('no-scroll'); // Enable scroll
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
            document.body.classList.remove('no-scroll'); // Enable scroll
        }
    }
}

function saveScheme() {
    const cables = document.querySelectorAll('.cable');
    const all_cables = [];

    const hardware = document.querySelectorAll('.hardware');
    const all_hardware = [];

    const crosses = document.querySelectorAll('.cross');
    const all_crosses = [];

    if (cables.length !== 0) {
        cables.forEach(cable => {
            const id = cable.id.replace('cable', ''); // Удаляем префикс из ID
            const left = parseInt(cable.style.left, 10); // Координата X
            const top = parseInt(cable.style.top, 10); // Координата Y
            const direction = cable.getAttribute('data-direction'); // Направление

            all_cables.push({ id, left, top, direction });
        });
    }

    if (hardware.length !== 0) {
        hardware.forEach(one_hardware => {
            const id = one_hardware.id.replace('hardware', ''); // Удаляем префикс из ID
            const left = parseInt(one_hardware.style.left, 10); // Координата X
            const top = parseInt(one_hardware.style.top, 10); // Координата Y
            const direction = one_hardware.getAttribute('data-direction'); // Направление

            all_hardware.push({ id, left, top, direction });
        });
    }

    if (crosses.length !== 0) {
        crosses.forEach(cross => {
            const id = cross.id.replace('cross', ''); // Удаляем префикс из ID
            const left = parseInt(cross.style.left, 10); // Координата X
            const top = parseInt(cross.style.top, 10); // Координата Y
            const direction = cross.getAttribute('data-direction'); // Направление

            all_crosses.push({ id, left, top, direction });
        });
    }

    const connections = {
        'cables': all_cables,
        'hardware': all_hardware,
        'crosses': all_crosses
    }

    fetch(`save/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(connections)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const schemeSelector = document.getElementById('scheme-selector');
            loadSchemeList(schemeSelector);
            showModal('Сохранено', 'Схема успешно сохранена');
        } else {
            showModal('Ошибка', 'Ошибка при сохранении схемы: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}


function setDirectionNameClass(nameDiv, direction) {
    if (direction === 'right') {nameDiv.classList.add("vertical-right");}
    else if (direction === 'left') {nameDiv.classList.add("vertical-left");}
}


function setModuleDimensions(moduleDiv, moduleLength, direction) {
    switch (direction) {
        case 'right':
        case 'left':
            moduleDiv.style.height = `${moduleLength}px`;
            break;
        case 'up':
        case 'down':
            moduleDiv.style.width = `${moduleLength}px`;
            break;
    }
}


function setModulePosition(cableDiv, moduleDiv, moduleLength, direction, cableLength) {
    let moduleLeft, moduleTop;
    switch (direction) {
        case 'right':
            moduleLeft = cableDiv.offsetWidth;
            moduleTop = cableLength;
            moduleDiv.style.width = `60px`;
            break;
        case 'left':
            moduleDiv.style.width = `60px`;
            moduleLeft = -moduleDiv.offsetWidth;
            moduleTop = cableLength;
            break;
        case 'up':
            moduleLeft = cableLength;
            moduleDiv.style.height = `60px`;
            moduleTop = -moduleDiv.offsetHeight;
            break;
        case 'down':
            moduleLeft = cableLength;
            moduleTop = cableDiv.offsetHeight;
            moduleDiv.style.height = `60px`;
            break;
    }
    return {moduleLeft, moduleTop};
}


function setFiberPosition(fiberDiv, moduleDiv, fIndex, direction) {
    switch (direction) {
        case 'right':
            fiberDiv.style.left = `${moduleDiv.offsetWidth - 2}px`;
            fiberDiv.style.top = `${(fIndex * 30 - 1)}px`;
            fiberDiv.style.width = `30px`;
            fiberDiv.style.height = `20px`;
            break;
        case 'left':
            fiberDiv.style.left = `-30px`;
            fiberDiv.style.top = `${(fIndex * 30 - 1)}px`;
            fiberDiv.style.width = `30px`;
            fiberDiv.style.height = `20px`;
            break;
        case 'up':
            fiberDiv.style.left = `${(fIndex * 30 - 1)}px`;
            fiberDiv.style.top = `-30px`;
            fiberDiv.style.width = `20px`;
            fiberDiv.style.height = `30px`;
            break;
        case 'down':
            fiberDiv.style.left = `${(fIndex * 30 - 1)}px`;
            fiberDiv.style.top = `${moduleDiv.offsetHeight - 2}px`;
            fiberDiv.style.width = `20px`;
            fiberDiv.style.height = `30px`;
            break;
    }
}


function setDimensions(cableDiv, cableLength, direction) {
    switch (direction) {
        case 'right':
        case 'left':
            cableDiv.style.height = `${cableLength - 10}px`;
            break;
        case 'up':
        case 'down':
            cableDiv.style.width = `${cableLength - 10}px`;
            break;
    }
}

function setModuleFibers(module, moduleDiv, direction){
    module.fibers.forEach((fiber, fIndex) => {
        const fiberDiv = document.createElement('div');
        fiberDiv.className = 'fiber';
        fiberDiv.id = fiber.id;
        fiberDiv.style.backgroundColor = fiber.color;
        fiberDiv.setAttribute('data-color', fiber.color);

        const fiberNumberDiv = document.createElement('div');
        fiberNumberDiv.className = 'fiberNumber';
        fiberNumberDiv.innerText = fIndex + 1; // Нумерация начинается с 1

        fiberDiv.appendChild(fiberNumberDiv);

        setFiberPosition(fiberDiv, moduleDiv, fIndex, direction);
        moduleDiv.appendChild(fiberDiv);
    });
}

function setCableModules(cable, direction, cableDiv, cableLength, DragManager){
    cable.modules.forEach((module, index) => {
        const moduleDiv = document.createElement('div');
        moduleDiv.className = 'module';
        moduleDiv.id = module.id;
        moduleDiv.style.backgroundColor = module.color;

        let moduleLength = module.fibers.length * 30 - 10; // Длина модуля
        if (moduleLength < 100){
            moduleLength = 100;
        }

        setModuleDimensions(moduleDiv, moduleLength, direction);

        moduleDiv.onmousedown = (e) => {
            e.stopPropagation();
            DragManager.makeObjectToDrag(e, moduleDiv);
        };

        cableDiv.appendChild(moduleDiv);
        moduleDiv.setAttribute('data-direction', direction);

        const {moduleLeft, moduleTop} = setModulePosition(cableDiv, moduleDiv, moduleLength, direction, cableLength);

        moduleDiv.style.left = `${moduleLeft - 1}px`;
        moduleDiv.style.top = `${moduleTop - 1}px`;

        const moduleName = document.createElement('div');
        moduleName.className = 'moduleName';
        setDirectionNameClass(moduleName, direction);
        moduleName.innerText = module.name;
        moduleDiv.appendChild(moduleName);

        cableLength = cableLength + moduleLength + 10; // Добавляем длину модуля к общей длине кабеля

        setModuleFibers(module, moduleDiv, direction);
    });
    return cableLength;
}

function setPortPosition(portDiv, hardwareDiv, pIndex, direction) {
    switch (direction) {
        case 'right':
            portDiv.style.left = `${hardwareDiv.offsetWidth - 2}px`;
            portDiv.style.top = `${(pIndex * 30 - 1)}px`;
            portDiv.style.width = `30px`;
            portDiv.style.height = `20px`;
            break;
        case 'left':
            portDiv.style.left = `-30px`;
            portDiv.style.top = `${(pIndex * 30 - 1)}px`;
            portDiv.style.width = `30px`;
            portDiv.style.height = `20px`;
            break;
        case 'up':
            portDiv.style.left = `${(pIndex * 30 - 1)}px`;
            portDiv.style.top = `-30px`;
            portDiv.style.width = `20px`;
            portDiv.style.height = `30px`;
            break;
        case 'down':
            portDiv.style.left = `${(pIndex * 30 - 1)}px`;
            portDiv.style.top = `${hardwareDiv.offsetHeight - 2}px`;
            portDiv.style.width = `20px`;
            portDiv.style.height = `30px`;
            break;
    }
}

function setHardwarePorts(hardware, direction, hardwareDiv){
    hardware.ports.forEach((port, index) => {
        const portDiv = document.createElement('div');
        portDiv.className = 'port';
        portDiv.id = port.id;

        portDiv.onmousedown = (e) => {
            e.stopPropagation();
            DragManager.makeObjectToDrag(e, portDiv);
        };

        const portNumberDiv = document.createElement('div');
        portNumberDiv.className = 'portNumber';
        portNumberDiv.innerText = index + 1; // Нумерация начинается с 1

        portDiv.appendChild(portNumberDiv);

        setPortPosition(portDiv, hardwareDiv, index, direction);
        hardwareDiv.appendChild(portDiv);
    });
}


function setLinearAdapterPosition(adapterDiv, crossDiv, aIndex, direction) {
    switch (direction) {
        case 'right':
        case 'left':
            adapterDiv.style.left = `-30px`;
            adapterDiv.style.top = `${(aIndex * 30 - 1)}px`;
            adapterDiv.style.width = `30px`;
            adapterDiv.style.height = `20px`;
            break;
        case 'up':
        case 'down':
            adapterDiv.style.left = `${(aIndex * 30 - 1)}px`;
            adapterDiv.style.top = `-30px`;
            adapterDiv.style.width = `20px`;
            adapterDiv.style.height = `30px`;
            break;
    }
}

function setStationAdapterPosition(adapterDiv, crossDiv, aIndex, direction) {
    switch (direction) {
        case 'right':
        case 'left':
            adapterDiv.style.left = `${crossDiv.offsetWidth - 2}px`;
            adapterDiv.style.top = `${(aIndex * 30 - 1)}px`;
            adapterDiv.style.width = `30px`;
            adapterDiv.style.height = `20px`;
            break;
        case 'up':
        case 'down':
            adapterDiv.style.left = `${(aIndex * 30 - 1)}px`;
            adapterDiv.style.top = `${crossDiv.offsetHeight}px`;
            adapterDiv.style.width = `20px`;
            adapterDiv.style.height = `30px`;
            break;
    }
}

function setCrossAdapters(cross, direction, crossDiv) {
    cross.linear_adapters.forEach((adapter, index) => {
        const adapterDiv = document.createElement('div');
        adapterDiv.className = 'linear-adapter';
        adapterDiv.id = adapter.id;

        const adapterNumberDiv = document.createElement('div');
        adapterNumberDiv.className = 'adapterNumber';
        adapterNumberDiv.innerText = index + 1; // Нумерация начинается с 1

        adapterDiv.appendChild(adapterNumberDiv);

        adapterDiv.onmousedown = (e) => {
            e.stopPropagation();
            DragManager.makeObjectToDrag(e, adapterDiv);
        };

        setLinearAdapterPosition(adapterDiv, crossDiv, index, direction);
        crossDiv.appendChild(adapterDiv);
    });

    cross.station_adapters.forEach((adapter, index) => {
        const adapterDiv = document.createElement('div');
        adapterDiv.className = 'station-adapter';
        adapterDiv.id = adapter.id;

        const adapterNumberDiv = document.createElement('div');
        adapterNumberDiv.className = 'adapterNumber';
        adapterNumberDiv.innerText = index + 1; // Нумерация начинается с 1

        adapterDiv.appendChild(adapterNumberDiv);

        adapterDiv.onmousedown = (e) => {
            e.stopPropagation();
            DragManager.makeObjectToDrag(e, adapterDiv);
        };

        setStationAdapterPosition(adapterDiv, crossDiv, index, direction);
        crossDiv.appendChild(adapterDiv);
    });
}

function setCross(container, cross, direction, DragManager) {
    const crossDiv = document.createElement('div');
    crossDiv.className = 'cross';
    crossDiv.id = cross.id;
    crossDiv.style.left = `${cross.left}px`;
    crossDiv.style.top = `${cross.top}px`;

    crossDiv.onmousedown = (e) => DragManager.makeObjectToDrag(e, crossDiv);

    const linearTypeDiv = document.createElement('div');
    linearTypeDiv.className = 'crossType linear';
    linearTypeDiv.innerText = `Тип ${cross.linear_type} ↑`;
    setDirectionNameClass(linearTypeDiv, direction);
    crossDiv.appendChild(linearTypeDiv);

    const stationTypeDiv = document.createElement('div');
    stationTypeDiv.className = 'crossType station';
    stationTypeDiv.innerText = `Тип ${cross.station_type} ↓`;
    setDirectionNameClass(stationTypeDiv, direction);
    crossDiv.appendChild(stationTypeDiv);

    container.appendChild(crossDiv);
    crossDiv.setAttribute('data-direction', direction);

    let crossLength = cross.linear_adapters.length * 30;
    if (crossLength < 100) {
        crossLength = 100;
    }

    setCrossAdapters(cross, direction, crossDiv);
    setDimensions(crossDiv, crossLength, direction);
}