document.addEventListener('DOMContentLoaded', function () {
    const avatarInput = document.getElementById('avatar');
    const deleteButton = document.getElementById('deleteButton');
    const saveButton = document.getElementById('saveButton');

    avatarInput.addEventListener('change', function () {
        if (avatarInput.files.length > 0) {
            deleteButton.style.display = 'none';
            saveButton.style.display = 'block';
        } else {
            deleteButton.style.display = 'none';
            saveButton.style.display = 'none';
        }
    });

    deleteButton.addEventListener('click', function () {
        // Здесь можно добавить код для удаления аватара
        // Затем скроем кнопки "Удалить аватар" и "Сохранить"
        deleteButton.style.display = 'none';
        saveButton.style.display = 'none';
        // Очистим значение input для файла, чтобы сбросить выбор изображения
        avatarInput.value = '';
    });
});