document.addEventListener('DOMContentLoaded', function() {
document.querySelectorAll('.create-record').forEach(function(button) {
    button.addEventListener('click', function() {
        var parentId = this.getAttribute('data-id');
        var url = '/admin/myapp/category/add/?parent=' + parentId;  // Измените app_name и model_name на ваши значения
        // Откроем модальное окно
        showAddAnotherPopup(window, url);
    });
});
});


function showAddAnotherPopup(triggeringLink, url) {
url = url + (url.indexOf('?') == -1 ? '?' : '&') + '_popup=1';
var win = window.open(url, 'add_category', 'height=500,width=800,resizable=yes,scrollbars=yes');
win.focus();

// Добавляем проверку на закрытие окна и обновление дерева
var interval = setInterval(function() {
    if (win.closed) {
        console.log('test')
        clearInterval(interval);
        // Сообщение родительскому окну для обновления страницы
        location.reload();
    }
}, 500);

return false;
}

