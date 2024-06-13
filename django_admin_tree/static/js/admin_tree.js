document.addEventListener('DOMContentLoaded', function() {
document.querySelectorAll('.create-record').forEach(function(button) {
    button.addEventListener('click', function() {
        console.log(window.location)
        var parentId = this.getAttribute('data-id');
        var create_url = this.getAttribute('data-url-template')
        var prent_params = this.getAttribute('data-parent-field')
        var url = `${create_url}?${prent_params}=` + parentId;
        console.log(url)
        // Откроем модальное окно
        showAddAnotherPopup(window, url);
    });
});
});


function showAddAnotherPopup(triggeringLink, url) {
url = url + (url.indexOf('?') == -1 ? '?' : '&') + '_popup=1';
var win = window.open(url, 'add_object', 'height=500,width=800,resizable=yes,scrollbars=yes');
win.focus();

// Добавляем проверку на закрытие окна и обновление дерева
var interval = setInterval(function() {
    if (win.closed) {
        clearInterval(interval);
        location.reload();
    }
}, 500);

return false;
}

