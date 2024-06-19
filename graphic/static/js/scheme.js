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
                if (this.dragObject.classList.contains('cable')
                || this.dragObject.classList.contains('hardware')
                || this.dragObject.classList.contains('cross')) {
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

                if (DragManager.dragObject.classList.contains('cable')
                || DragManager.dragObject.classList.contains('hardware')
                || DragManager.dragObject.classList.contains('cross')) {
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

        cableLength = setCableModules(cable, direction, cableDiv, cableLength, DragManager);

        setDimensions(cableDiv, cableLength, direction);

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

            cableDiv.removeAttribute("style");
            cableDiv.innerHTML = "";
            setCable(container, cable, selectedDirection, cableDiv, DragManager);

            updateConnectionLines(cableDiv);
        });

        selectContainer.appendChild(directionSelect);
        cableDiv.appendChild(selectContainer);
    }

    function setHardware(container, hardware, direction, hardwareDiv, DragManager) {
        hardwareDiv.style.left = `${hardware.left}px`;
        hardwareDiv.style.top = `${hardware.top}px`;

        hardwareDiv.onmousedown = (e) => DragManager.makeObjectToDrag(e, hardwareDiv);

        const hardwareName = document.createElement('div');
        hardwareName.className = 'hardwareName';
        setDirectionNameClass(hardwareName, direction);
        hardwareName.innerText = hardware.marking;
        hardwareDiv.appendChild(hardwareName);

        container.appendChild(hardwareDiv);
        hardwareDiv.setAttribute('data-direction', direction);

        let hardwareLength = hardware.ports.length * 30; // Длина модуля
        if (hardwareLength < 100){
            hardwareLength = 100;
        }

        setHardwarePorts(hardware, direction, hardwareDiv);
        setDimensions(hardwareDiv, hardwareLength, direction);

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

            hideAllConnectionLines(hardwareDiv);

            hardware.left = parseInt(hardwareDiv.style.left, 10) || 0;
            hardware.top = parseInt(hardwareDiv.style.top, 10) || 0;

            hardwareDiv.removeAttribute("style");
            hardwareDiv.innerHTML = "";
            setHardware(container, hardware, selectedDirection, hardwareDiv, DragManager);

            updateConnectionLines(hardwareDiv);
        });

        selectContainer.appendChild(directionSelect);
        hardwareDiv.appendChild(selectContainer);
    }

    const container = document.getElementById('network-container');

    // Создаем SVG элемент для соединительных линий
    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.style.position = "absolute";
    svg.style.top = 0;
    svg.style.left = 0;
    container.appendChild(svg);

    const cables = JSON.parse(document.getElementById('graphic_json').textContent);
    if (cables.length !== 0) {
        cables.forEach(cable => {
        const cableDiv = document.createElement('div');
        cableDiv.className = 'cable';
        cableDiv.id = cable.id;

        setCable(container, cable, cable.direction, cableDiv, DragManager);
        });
    }

    const hardware = JSON.parse(document.getElementById('hardware_json').textContent);

    if (hardware.length !== 0) {
        hardware.forEach(one_hardware => {
            const hardwareDiv = document.createElement('div');
            hardwareDiv.className = 'hardware';
            hardwareDiv.id = one_hardware.id;
            setHardware(container, one_hardware, one_hardware.direction, hardwareDiv, DragManager);
        });
    }

    const crosses = JSON.parse(document.getElementById('crosses_json').textContent);

    if (crosses.length !== 0) {
        crosses.forEach(cross => {
            setCross(container, cross, cross.direction, DragManager);
        });
    }

    // Функция для создания соединительных линий
    function createConnectionLine(object1_id, object2_id, cable1_id, cable2_id) {
        const container = document.getElementById('network-container');
        const containerRect = container.getBoundingClientRect();

        const object1 = document.getElementById(object1_id); // Получите нужный элемент волокна
        const object2 = document.getElementById(object2_id); // Получите нужный элемент волокна
        const object1Rect = object1.getBoundingClientRect();
        const object2Rect = object2.getBoundingClientRect();

        const x1 = object1Rect.left + object1.offsetWidth / 2 - containerRect.left;
        const y1 = object1Rect.top + object2.offsetHeight / 2 - containerRect.top;
        const x2 = object2Rect.left + object2.offsetWidth / 2 - containerRect.left;
        const y2 = object2Rect.top + object2.offsetHeight / 2 - containerRect.top;

        // Создаем контейнер для линий
        const lineGroup = document.createElementNS(svgNS, 'g');
        lineGroup.classList.add(`line-${object1_id}`);
        lineGroup.classList.add(`line-${object2_id}`);
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
        const object1Direction = object1.parentElement.dataset.direction;
        const object2Direction = object2.parentElement.dataset.direction;

        if ((object1Direction === 'left' || object1Direction === 'right') &&
            (object2Direction === 'left' || object2Direction === 'right'))
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
        else if ((object1Direction === 'down' || object1Direction === 'up') &&
            (object2Direction === 'down' || object2Direction === 'up'))
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
        else if (object1Direction === 'down' || object1Direction === 'up')
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
        createLineWithOutline(points1, object1.dataset.color || '#EAD200');
        createLineWithOutline(points2, object2.dataset.color || '#EAD200');

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
    function hideAllConnectionLines(element) {
        const container = document.getElementById('network-container');

        // Находим все группы линий соединения, связанные с перемещаемым кабелем
        const lineGroups = document.querySelectorAll(`.line-${element.id}`);
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

    const connections = JSON.parse(document.getElementById('connections_json').textContent);
    if (connections.length !== 0) {
        connections.forEach(connection => {
            createConnectionLine(connection.start, connection.end, connection.object_start, connection.object_end)
        });
    }


    const print_button = document.getElementById('print-button');
    print_button.addEventListener('click', function() {
        window.print();
    });

    const screenshot_button = document.getElementById('screenshot-button');
    screenshot_button.addEventListener('click', function() {
        const screen_content = document.getElementById('network-container');
        html2canvas(screen_content).then(canvas => {
            const link = document.createElement('a');
            link.href = canvas.toDataURL('image/png');
            const download_name = document.getElementById('center-name').textContent.trim();
            link.download = `Схема для ${download_name}`;
            link.click();
        });
    });
});
