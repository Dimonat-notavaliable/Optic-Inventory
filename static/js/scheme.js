

document.addEventListener("DOMContentLoaded", function() {
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

        // Установка начальной позиции в зависимости от направления
        switch (cable.direction) {
            case 'right':
                cableDiv.style.left = `100px`;
                cableDiv.style.top = `200px`;
                break;
            case 'left':
                cableDiv.style.left = `${container.offsetWidth - 200}px`;
                cableDiv.style.top = `200px`;
                break;
            case 'up':
                cableDiv.style.left = `${container.offsetWidth / 3}px`;
                cableDiv.style.top = `${container.offsetHeight - 100}px`;
                break;
            case 'down':
                cableDiv.style.left = `${container.offsetWidth / 3}px`;
                cableDiv.style.top = `10px`;
                break;
        }

        cableDiv.onmousedown = (e) => DragManager.makeObjectToDrag(e, cableDiv);

        const cableName = document.createElement('div');
        cableName.className = 'cableName';
        if (cable.direction == 'right'){
            cableName.classList.add("vertical-right")
        }
        if (cable.direction == 'left'){
            cableName.classList.add("vertical-left")
        }
        cableName.innerText = cable.name;
        cableDiv.appendChild(cableName);

        container.appendChild(cableDiv);
        cableDiv.setAttribute('data-direction', cable.direction);

        let cableLength = 0; // Переменная для общей длины кабеля

        cable.modules.forEach((module, index) => {
            const moduleDiv = document.createElement('div');
            moduleDiv.className = 'module';
            moduleDiv.id = module.id;
            moduleDiv.style.backgroundColor = module.color;


            let moduleLength = module.fibers.length * 30 - 10; // Длина модуля
            if (moduleLength < 100){
                moduleLength = 100;
            }

            switch (cable.direction) {
                case 'right':
                case 'left':
                    moduleDiv.style.height = `${moduleLength}px`;
                    break;
                case 'up':
                case 'down':
                    moduleDiv.style.width = `${moduleLength}px`;
                    break;
            }


            moduleDiv.onmousedown = (e) => {
                e.stopPropagation();
                DragManager.makeObjectToDrag(e, moduleDiv);
            };

            cableDiv.appendChild(moduleDiv);

            let moduleLeft, moduleTop;

            switch (cable.direction) {
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

            moduleDiv.style.left = `${moduleLeft - 1}px`;
            moduleDiv.style.top = `${moduleTop - 1}px`;

            const moduleName = document.createElement('div');
            moduleName.className = 'moduleName';
            if (cable.direction == 'right'){
                moduleName.classList.add("vertical-right")
            }
            if (cable.direction == 'left'){
                moduleName.classList.add("vertical-left")
            }
            moduleName.innerText = module.name;
            moduleDiv.appendChild(moduleName);

            cableLength = cableLength + moduleLength + 10; // Добавляем длину модуля к общей длине кабеля

            module.fibers.forEach((fiber, fIndex) => {
                const fiberDiv = document.createElement('div');
                fiberDiv.className = 'fiber';
                fiberDiv.id = fiber.id;
                fiberDiv.style.backgroundColor = fiber.color;
                fiberDiv.setAttribute('data-color', fiber.color);


                switch (cable.direction) {
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

                moduleDiv.appendChild(fiberDiv);
            });

        });

        // Обновляем высоту или ширину кабеля после добавления всех модулей
        switch (cable.direction) {
            case 'right':
            case 'left':
                cableDiv.style.height = `${cableLength - 10}px`;
                break;
            case 'up':
            case 'down':
                cableDiv.style.width = `${cableLength - 10}px`;
                break;
        }
    });

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
                    removeAllConnectionLines(this.dragObject);
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
    // Функция для создания соединительных линий
    function createConnectionLine(fiber1, fiber2) {
        const container = document.getElementById('network-container');
        const containerRect = container.getBoundingClientRect();
        const fiber1Rect = fiber1.getBoundingClientRect();
        const fiber2Rect = fiber2.getBoundingClientRect();

        const x1 = fiber1Rect.left + fiber1.offsetWidth / 2 - containerRect.left;
        const y1 = fiber1Rect.top + fiber1.offsetHeight / 2 - containerRect.top;
        const x2 = fiber2Rect.left + fiber2.offsetWidth / 2 - containerRect.left;
        const y2 = fiber2Rect.top + fiber2.offsetHeight / 2 - containerRect.top;

        // Создаем контейнер для линий
        const lineGroup = document.createElementNS(svgNS, 'g');
        lineGroup.classList.add(`line-${fiber1.id}`);
        lineGroup.classList.add(`line-${fiber2.id}`);
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
            (fiber2Direction === 'down' || fiber2Direction === 'up')) {
            points1.push([x1, y1]);
            points1.push([x1, (y1 + y2) / 2]);
            points1.push([(x1 + x2) / 2, (y1 + y2) / 2]);

            points1.push([(x1 + x2) / 2, (y1 + y2) / 2]);
            points2.push([x2, (y1 + y2) / 2]);
            points2.push([x2, y2]);

            // Создание круга в середине линии
            midX = (x1 + x2) / 2;
            midY = (y1 + y2) / 2;
        }
        else if (fiber1Direction === 'down' || fiber1Direction === 'up') {
            points1.push([x1, y1]);
            points1.push([x1, y2]);

            points2.push([x1, y2]);
            points2.push([x2, y2]);

            // Создание круга в середине линии
            midX = x1;
            midY = y2;
        }
        else {
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

    // Функция для обновления соединительных линий
    function updateConnectionLines(fiber) {
        console.log('hello')
        const fiber1 = document.getElementById('fiber1'); // Получите нужный элемент волокна
        const fiber2 = document.getElementById('fiber20'); // Получите нужный элемент волокна
        createConnectionLine(fiber1, fiber2);

        const fiber3 = document.getElementById('fiber2'); // Получите нужный элемент волокна
        const fiber4 = document.getElementById('fiber22'); // Получите нужный элемент волокна
        createConnectionLine(fiber3, fiber4);

        const fiber5 = document.getElementById('fiber5'); // Получите нужный элемент волокна
        const fiber6 = document.getElementById('fiber21'); // Получите нужный элемент волокна
        createConnectionLine(fiber5, fiber6);

        const fiber7 = document.getElementById('fiber6'); // Получите нужный элемент волокна
        const fiber8 = document.getElementById('fiber23'); // Получите нужный элемент волокна
        createConnectionLine(fiber7, fiber8);
    }
    // Функция для удаления всех соединительных линий, связанных с кабелем
    function removeAllConnectionLines(cable) {
        console.log('removeAllConnectionLines working')
        const fibers = cable.querySelectorAll('.fiber');
        fibers.forEach(fiber => {
            removeConnectionLines(fiber);
        });
    }

    // Функция для удаления старых соединительных линий
    function removeConnectionLines(fiber) {
        console.log('removeConnectionLines working')
        const lineClass = `line-${fiber.id}`;
        const lines = document.querySelectorAll(`.${lineClass}`);
        console.log(lines);
        lines.forEach(line => line.remove());
    }
    const fiber1 = document.getElementById('fiber1'); // Получите нужный элемент волокна
    const fiber2 = document.getElementById('fiber20'); // Получите нужный элемент волокна
    createConnectionLine(fiber1, fiber2);

    const fiber3 = document.getElementById('fiber2'); // Получите нужный элемент волокна
    const fiber4 = document.getElementById('fiber22'); // Получите нужный элемент волокна
    createConnectionLine(fiber3, fiber4);

    const fiber5 = document.getElementById('fiber5'); // Получите нужный элемент волокна
    const fiber6 = document.getElementById('fiber21'); // Получите нужный элемент волокна
    createConnectionLine(fiber5, fiber6);

    const fiber7 = document.getElementById('fiber6'); // Получите нужный элемент волокна
    const fiber8 = document.getElementById('fiber23'); // Получите нужный элемент волокна
    createConnectionLine(fiber7, fiber8);
});
