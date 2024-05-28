
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

    makeObjectToDrag(obj) {
        if (obj) {
            this.dragObject = obj;
            document.addEventListener('mousemove', this.moving.bind(this));
            document.addEventListener('mouseup', this.drop.bind(this));
            this.dragObject.classList.add('moving');
            this.getCursorPos(window.event);
            this.offsetX = this.cursor.x - this.dragObject.offsetLeft;
            this.offsetY = this.cursor.y - this.dragObject.offsetTop;
        }
    },

    moving(e) {
        this.getCursorPos(e);
        if (this.dragObject) {
            const left = this.cursor.x - this.offsetX;
            const top = this.cursor.y - this.offsetY;
            this.dragObject.style.left = `${left}px`;
            this.dragObject.style.top = `${top}px`;
        }
    },

    drop() {
        if (this.dragObject) {
            this.dragObject.classList.remove('moving');

            const currentLeft = parseInt(getComputedStyle(this.dragObject).left, 10);
            const currentTop = parseInt(getComputedStyle(this.dragObject).top, 10);

            const newLeft = Math.round(currentLeft / 10) * 10;
            const newTop = Math.round(currentTop / 10) * 10;

            this.dragObject.style.left = `${newLeft}px`;
            this.dragObject.style.top = `${newTop}px`;

            document.removeEventListener('mousemove', this.moving.bind(this));
            document.removeEventListener('mouseup', this.drop.bind(this));

            this.dragObject = null;
        }
    }
};