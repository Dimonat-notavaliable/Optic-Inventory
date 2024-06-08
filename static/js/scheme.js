function getQueryParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}


function loadSchemeList(schemeSelector){
    // Загрузка списка схем
    fetch(`all/`)
        .then(response => response.json())
        .then(data => {
            schemeData = data.schemes;
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

function saveScheme() {
    const cables = document.querySelectorAll('.cable');
    const connections = [];

    cables.forEach(cable => {
        const id = cable.id.replace('cable', ''); // Удаляем префикс "cable" из ID
        const left = parseInt(cable.style.left, 10); // Координата X
        const top = parseInt(cable.style.top, 10); // Координата Y
        const direction = cable.getAttribute('data-direction'); // Направление кабеля

        connections.push({ id, left, top, direction });
    });

    fetch(`save/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, // Не забудьте добавить CSRF-токен
        },
        body: JSON.stringify({ connections })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Схема успешно сохранена');
        } else {
            alert('Ошибка при сохранении схемы: ' + data.message);
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


function setCableDimensions(cableDiv, cableLength, direction) {
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

        setFiberPosition(fiberDiv, moduleDiv, fIndex, direction);
        moduleDiv.appendChild(fiberDiv);
    });
}

function setCableModules(cable, direction, cableDiv, cableLength){
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

document.addEventListener("DOMContentLoaded", function() {
    // Вызов функции сохранения,привязан к нажатию кнопки
    document.getElementById('save-button').addEventListener('click', saveScheme);

    const schemeSelectorContainer = document.getElementById('scheme-selector-container');
    const schemeSelector = document.getElementById('scheme-selector');
    const dropdownButton = document.getElementById('dropdown-scheme-selector');

    loadSchemeList(schemeSelector);

    // Обработчик для загрузки списка схем при клике на кнопку
    dropdownButton.addEventListener('click', function() {
        schemeSelectorContainer.classList.toggle('show');
    });

    // Закрыть dropdown, если пользователь кликает вне его области
    window.addEventListener('click', function(event) {
        if (!event.target.matches('#dropdown-scheme-selector') && !event.target.matches('.fa-clock-rotate-left')) {
            schemeSelectorContainer.classList.remove('show');
        }
    });

    // Обработчик изменения селектора схем
    schemeSelector.addEventListener('change', function() {
        const selectedSchemeId = schemeSelector.value;
        // Обновление URL с новым идентификатором схемы
        loadScheme(selectedSchemeId);
    });

    // Функция для загрузки выбранной схемы
    function loadScheme(schemeId) {
        let url = new URL(window.location);
        url.searchParams.set('scheme_id', schemeId);
        window.location.href = url.toString();
    }

     const DragManager = {
        cursor: { x: 0, y: 0 },
        dragObject: null,
        offsetX: 0,
        offsetY: 0,

        getCursorPos(e) {
            if (e.pageX || e.pageY) {
                this.cursor.x = e.pageX;
                this.cursor.y = e.pageY;
            } else {
                const de = document.documentElement;
                const db = document.body;
                this.cursor.x = e.clientX + (de.scrollLeft || db.scrollLeft) - (de.clientLeft || 0);
                this.cursor.y = e.clientY + (de.scrollTop || db.scrollTop) - (de.clientTop || 0);
            }
        },

        makeObjectToDrag(e, obj) {
            if (obj && !obj.classList.contains('module')) {
                e.preventDefault();
                this.dragObject = obj;
                document.addEventListener('mousemove', this.moving);
                document.addEventListener('mouseup', this.drop);
                this.dragObject.classList.add('moving');
                this.getCursorPos(e);
                this.offsetX = this.cursor.x - this.dragObject.offsetLeft;
                this.offsetY = this.cursor.y - this.dragObject.offsetTop;

                // Удаляем старые линии соединения
                if (this.dragObject.classList.contains('cable')) {
                    hideAllConnectionLines(this.dragObject);
                }
            }
        },

        moving(e) {
            DragManager.getCursorPos(e);
            if (DragManager.dragObject) {
                const left = DragManager.cursor.x - DragManager.offsetX;
                const top = DragManager.cursor.y - DragManager.offsetY;
                DragManager.dragObject.style.left = `${left}px`;
                DragManager.dragObject.style.top = `${top}px`;

                if (DragManager.dragObject.classList.contains('cable')) {
                    const cable = cables.find(cable => cable.id === DragManager.dragObject.id);
                }
            }
        },

        drop() {
            if (DragManager.dragObject) {
                DragManager.dragObject.classList.remove('moving');

                const currentLeft = parseInt(getComputedStyle(DragManager.dragObject).left, 10);
                const currentTop = parseInt(getComputedStyle(DragManager.dragObject).top, 10);

                const newLeft = Math.round(currentLeft / 10) * 10;
                const newTop = Math.round(currentTop / 10) * 10;

                DragManager.dragObject.style.left = `${newLeft}px`;
                DragManager.dragObject.style.top = `${newTop}px`;

                if (DragManager.dragObject.classList.contains('cable')) {
                    const cable = cables.find(cable => cable.id === DragManager.dragObject.id);
                    updateConnectionLines(DragManager.dragObject);
                }

                document.removeEventListener('mousemove', DragManager.moving);
                document.removeEventListener('mouseup', DragManager.drop);

                DragManager.dragObject = null;
            }
        }
    };

    function setCable(container, cable, direction, cableDiv, DragManager){
        cableDiv.style.left = `${cable.left}px`;
        cableDiv.style.top = `${cable.top}px`;

        cableDiv.onmousedown = (e) => DragManager.makeObjectToDrag(e, cableDiv);

        const cableName = document.createElement('div');
        cableName.className = 'cableName';
        setDirectionNameClass(cableName, direction);
        cableName.innerText = cable.name;
        cableDiv.appendChild(cableName);

        container.appendChild(cableDiv);
        cableDiv.setAttribute('data-direction', direction);

        let cableLength = 0; // Переменная для общей длины кабеля

        cableLength = setCableModules(cable, direction, cableDiv, cableLength);

        setCableDimensions(cableDiv, cableLength, direction);

        // Создаем контейнер для выпадающего списка
        const selectContainer = document.createElement('div');
        selectContainer.className = 'select-container';

        const directionSelect = document.createElement('select');
        directionSelect.innerHTML = `
            <option value="right">▶Вправо</option>
            <option value="left">◀Влево</option>
            <option value="up">▲Вверх</option>
            <option value="down">▼Вниз</option>
        `;

        directionSelect.value = direction;

        directionSelect.addEventListener('mousedown', function(e) {
        e.stopPropagation(); // Останавливаем распространение события на родительские элементы
        });

        directionSelect.addEventListener('change', function() {
            const selectedDirection = this.value;
            const container = document.getElementById('network-container');

            hideAllConnectionLines(cableDiv);

            cable.left = parseInt(cableDiv.style.left, 10) || 0;
            cable.top = parseInt(cableDiv.style.top, 10) || 0;

            // Далее можете вызвать функцию setPositionAndDirection для обновления позиции и направления кабеля
            cableDiv.removeAttribute("style");
            cableDiv.innerHTML = "";
            setCable(container, cable, selectedDirection, cableDiv, DragManager);
            // Если нужно обновить соединительные линии, вызовите соответствующую функцию

            updateConnectionLines(cableDiv);
        });

        selectContainer.appendChild(directionSelect);
        cableDiv.appendChild(selectContainer);
    }

    const container = document.getElementById('network-container');
    const cables = JSON.parse(document.getElementById('graphic_json').textContent);

    if (cables.length === 0) {
        return; // Нет кабелей для отображения
    }


    // Создаем SVG элемент для соединительных линий
    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.style.position = "absolute";
    svg.style.top = 0;
    svg.style.left = 0;
    container.appendChild(svg);

    cables.forEach(cable => {
        const cableDiv = document.createElement('div');
        cableDiv.className = 'cable';
        cableDiv.id = cable.id;

        setCable(container, cable, cable.direction, cableDiv, DragManager);
    });


    // Функция для создания соединительных линий
    function createConnectionLine(fiber1_id, fiber2_id, cable1_id, cable2_id) {
        const container = document.getElementById('network-container');
        const containerRect = container.getBoundingClientRect();

        const fiber1 = document.getElementById(fiber1_id); // Получите нужный элемент волокна
        const fiber2 = document.getElementById(fiber2_id); // Получите нужный элемент волокна
        const fiber1Rect = fiber1.getBoundingClientRect();
        const fiber2Rect = fiber2.getBoundingClientRect();

        const x1 = fiber1Rect.left + fiber1.offsetWidth / 2 - containerRect.left;
        const y1 = fiber1Rect.top + fiber1.offsetHeight / 2 - containerRect.top;
        const x2 = fiber2Rect.left + fiber2.offsetWidth / 2 - containerRect.left;
        const y2 = fiber2Rect.top + fiber2.offsetHeight / 2 - containerRect.top;

        // Создаем контейнер для линий
        const lineGroup = document.createElementNS(svgNS, 'g');
        lineGroup.classList.add(`line-${fiber1_id}`);
        lineGroup.classList.add(`line-${fiber2_id}`);
        lineGroup.classList.add(`line-${cable1_id}`);
        lineGroup.classList.add(`line-${cable2_id}`);
        lineGroup.classList.add('connection-group');
        svg.appendChild(lineGroup);

        // Функция для создания линии с обводкой
        function createLineWithOutline(points, color) {
            // Создаем линию для обводки
            const outline = document.createElementNS(svgNS, 'polyline');
            outline.setAttribute('stroke', 'black');
            outline.setAttribute('stroke-width', '7'); // Толщина линии + 2 пикселя для обводки
            outline.setAttribute('fill', 'none');
            outline.setAttribute('points', points.map(p => p.join(',')).join(' '));
            lineGroup.appendChild(outline);

            // Создаем основную линию
            const line = document.createElementNS(svgNS, 'polyline');
            line.setAttribute('stroke', color);
            line.setAttribute('stroke-width', '5'); // Толщина основной линии
            line.setAttribute('fill', 'none');
            line.classList.add('connection-line');
            line.setAttribute('points', points.map(p => p.join(',')).join(' '));
            lineGroup.appendChild(line);
        }

        // Линии изгибаются под прямыми углами в зависимости от направления
        const points1 = [];
        const points2 = [];

        // Создание круга в середине линии
        let midX = 0;
        let midY = 0;

        // Проверка направления кабелей
        const fiber1Direction = fiber1.parentElement.parentElement.dataset.direction;
        const fiber2Direction = fiber2.parentElement.parentElement.dataset.direction;

        if ((fiber1Direction === 'left' || fiber1Direction === 'right') &&
            (fiber2Direction === 'left' || fiber2Direction === 'right'))
        {
            points1.push([x1, y1]);
            points1.push([(x1 + x2) / 2, y1]);
            points1.push([(x1 + x2) / 2, (y1 + y2) / 2]);

            points2.push([(x1 + x2) / 2, (y1 + y2) / 2]);
            points2.push([(x1 + x2) / 2, y2]);
            points2.push([x2, y2]);

            // Создание круга в середине линии
            midX = (x1 + x2) / 2;
            midY = (y1 + y2) / 2;
        }
        else if ((fiber1Direction === 'down' || fiber1Direction === 'up') &&
            (fiber2Direction === 'down' || fiber2Direction === 'up'))
        {
            points1.push([x1, y1]);
            points1.push([x1, (y1 + y2) / 2]);
            points1.push([(x1 + x2) / 2, (y1 + y2) / 2]);

            points2.push([(x1 + x2) / 2, (y1 + y2) / 2]);
            points2.push([x2, (y1 + y2) / 2]);
            points2.push([x2, y2]);

            // Создание круга в середине линии
            midX = (x1 + x2) / 2;
            midY = (y1 + y2) / 2;
        }
        else if (fiber1Direction === 'down' || fiber1Direction === 'up')
        {
            points1.push([x1, y1]);
            points1.push([x1, y2]);

            points2.push([x1, y2]);
            points2.push([x2, y2]);

            // Создание круга в середине линии
            midX = x1;
            midY = y2;
        }
        else
        {
            points1.push([x1, y1]);
            points1.push([x2, y1]);

            points2.push([x2, y1]);
            points2.push([x2, y2]);

            midX = x2;
            midY = y1;
        }

        // Создаем линии с обводкой
        createLineWithOutline(points1, fiber1.dataset.color || 'black');
        createLineWithOutline(points2, fiber2.dataset.color || 'black');

        const circle = document.createElementNS(svgNS, 'circle');
        circle.setAttribute('cx', midX);
        circle.setAttribute('cy', midY);
        circle.setAttribute('r', '5');  // Радиус круга
        circle.setAttribute('fill', 'white');
        circle.setAttribute('stroke', 'black');
        circle.setAttribute('stroke-width', '2');
        circle.classList.add('mid-circle');

        lineGroup.appendChild(circle);
    }

    // Функция для скрытия всех соединительных линий, связанных с кабелем
    function hideAllConnectionLines(cable) {
        const container = document.getElementById('network-container');

        // Находим все группы линий соединения, связанные с перемещаемым кабелем
        const lineGroups = document.querySelectorAll(`.line-${cable.id}`);
        // Перебираем все найденные группы линий
        lineGroups.forEach(lineGroup => {
            // Скрываем группу линий, устанавливая её display на none
            lineGroup.style.display = 'none';
        });
    }

    function updateConnectionLines(cable) {
        const container = document.getElementById('network-container');

        // Находим все группы линий соединения, связанные с перемещаемым кабелем
        const lineGroups = document.querySelectorAll(`.line-${cable.id}`);

        // Перерисовываем каждую группу линий соединения
        lineGroups.forEach(lineGroup => {
            // Получаем информацию о волокнах или кабелях, связанных с этой группой
            const fiber1Id = lineGroup.classList[0].replace('line-', '');
            const fiber2Id = lineGroup.classList[1].replace('line-', '');
            const cable1Id = lineGroup.classList[2].replace('line-', '');
            const cable2Id = lineGroup.classList[3].replace('line-', '');

            // Удаляем текущую группу линий
            lineGroup.remove();
            createConnectionLine(fiber1Id, fiber2Id, cable1Id, cable2Id);
        });
    }

    const weldings = JSON.parse(document.getElementById('welding_json').textContent);
    weldings.forEach(welding => {
        createConnectionLine(welding.start, welding.end, welding.cable_start, welding.cable_end)
    });


    const print_button = document.getElementById('print-button');
    print_button.addEventListener('click', function() {
        window.print();
    });

    const screenshot_button = document.getElementById('screenshot-button');
    screenshot_button.addEventListener('click', function() {
        const screen_content = document.getElementById('network-container');
         const schemeSelector = document.getElementById('scheme-selector');
        const selectedSchemeId = schemeSelector.value;
        const selectedScheme = schemeData.find(scheme => scheme.id == selectedSchemeId);
        const lastChangeTime = selectedScheme ? selectedScheme.last_change : 'unknown-time';
        html2canvas(screen_content).then(canvas => {
            const link = document.createElement('a');
            link.href = canvas.toDataURL('image/png');
            const download_name = document.getElementById('center-name').textContent.trim();
            link.download = `Схема для ${download_name} от ${lastChangeTime}.png`;
            link.click();
        });
    });
});
