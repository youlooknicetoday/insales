function getPageProductsIds() {
    const ids = [];
    let table = document.querySelector('tbody[data-editable-cells]');
    table.querySelectorAll('a[data-pjax-fragment=".body-div"]')
        .forEach((item) => {
            ids.push(item.getAttribute('href').split('/')[3]);
    })
    return ids
}

function getAllProductsIds() {
    const ids = [];
    let nextPage = document.querySelector('.next_page');
    ids.push(...getPageProductsIds());
    if (nextPage) {
        let allPages = parseInt(document.querySelector('.simple-pager > b').textContent.split('/')[1]) - 1;
        let observer = new MutationObserver(mutations => {
            mutations.forEach((mutation) => {
                if (mutation.oldValue === 'spinner-screen') {
                    ids.push(...getPageProductsIds());
                    nextPage = document.querySelector('.next_page');
                    allPages === 0 ? observer.disconnect() : nextPage.click(); allPages --;
                }
            });
        });
        observer.observe(document.getElementById('screen'),
            {attributes: true, attributeFilter: ['class'], attributeOldValue: true})
        nextPage.click();
        allPages --;
    }
    return ids
}
