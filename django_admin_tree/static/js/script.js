'use strict';
// import * as mod from "admin/js/admin/RelatedObjectLookups.js";
//
// var popupIndex = 0
// function addPopupIndex(name) {
//         return name + "__" + (popupIndex + 1);
//     }
//
// function showAdminPopup(triggeringLink, name_regexp, add_popup) {
//         const name = addPopupIndex(triggeringLink.id.replace(name_regexp, ''));
//         console.log('name', name)
//         console.log('triggeringLink.href', triggeringLink.href)
//         var link = triggeringLink.href
//         link = 'http://127.0.0.1:8000/admin/myapp/category/add/'
//         var  href = new URL(link);
//         if (add_popup) {
//             href.searchParams.set('_popup', 1);
//             href.searchParams.set('parent_id', 1);
//         }
//         console.log('href', href)
//
//         const win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
//         relatedWindows.push(win);
//         win.focus();
//         return false;
//     }

// function showRelatedObjectLookupPopup(triggeringLink) {
//         return showAdminPopup(triggeringLink, /^lookup_/, true);
//     }

function test(element, evenv) {
    const object_id = element.id
    const link = 'http://127.0.0.1:8000/admin/myapp/category/add/'
    const href = new URL(link);
    href.searchParams.set('_popup', 1);
    href.searchParams.set('parent_id', 1);
    const win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus()
    // return showRelatedObjectLookupPopup(a);
}
