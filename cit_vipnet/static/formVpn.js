const lic = document.querySelector('#id_license_act');
const formDropdownItems = document.querySelector('.form__dropdown-items');
const addLic = document.querySelector('#addLic');

const api = new Api(apiUrl);


function Licenses() {

    // клик по элементам с сервера
    const dropdown = (e) => {
        if (e.target.classList.contains('dropdown-item')) {
            lic.value = e.target.getAttribute('data-val-act');
            lic.date = e.target.getAttribute('data-val-date');
            lic.amount = e.target.getAttribute('data-val-amount');
            lic.distr = e.target.getAttribute('data-val-distr');
            formDropdownItems.style.display = ''
            licenses.addLicense();
        }
    };
    // Добавление элемента из инпута
    const addLicense = (e) => {

        if(lic.value) {
            const data = getValue();
            if (data.name) {
                document.getElementById('id_license_act').value = data.name;
            }
            if (data.date !== null) {
                document.getElementById('id_license_date').value = data.date;
                document.getElementById('id_license_date').readOnly = true;
            }
            else {
                document.getElementById('id_license_date').readOnly = false;
            }
            if (data.amount !== null) {
                document.getElementById('id_license_amount').value = data.amount;
                document.getElementById('id_license_amount').readOnly = true;
            }
            else {
                document.getElementById('id_license_amount').value = 1;
                document.getElementById('id_license_amount').readOnly = false;
            }
            try {
                document.getElementById('id_license_distributor').value = data.distr;
            }
            catch {
                document.getElementById('id_license_distributor').getElementsByTagName(
                'option')[0].selected = true;
            }

        }
    };
    // получение данных из инпутов для добавления
    const getValue = (e) => {
        const data = {
            name: lic.value,
            date: lic.date,
            amount: lic.amount,
            distr: lic.distr,
        };
        return data;
    };
    // очистка инпута
    const clearValue = (input) => {
        input.value = '';
    };
    return {
        clearValue,
        getValue,
        addLicense,
        dropdown
    }
}

const cbEventInput = (elem) => {
    return api.getLicense(elem.target.value).then( e => {
        if(e.length !== 0 ) {
            const items = e.map( elem => {
                return `<li><a class="dropdown-item" id="addLic"
                        data-val-act = "${elem.act}"
                        data-val-amount="${elem.amount}"
                        data-val-distr="${elem.distributor}"
                        data-val-date="${elem.date}"">${elem.act}</a></li>`

            }).join(' ')
            formDropdownItems.style.display = 'block';
            formDropdownItems.innerHTML = items + `<li>
                           <a class="dropdown-item" id="addLic"
                           data-val-act="${elem.target.value}">Новая лицензия...</a></li>`;
        } else {
            const items = `<li>
                           <a class="dropdown-item" id="addLic"
                           data-val-act="${elem.target.value}">Новая лицензия...</a></li>`
            formDropdownItems.style.display = 'block';
            formDropdownItems.innerHTML = items;
        }
    })
    .catch( e => {
        console.log(e)
    })
};

const eventInput = debouncing(cbEventInput, 1000);

// вешаем апи
lic.addEventListener('input', eventInput);
const licenses = Licenses();
// вешаем слушатель на элементы с апи
formDropdownItems.addEventListener('click', licenses.dropdown);
// вешаем слушатель на кнопку
