const counterId = document.querySelector('#counter');

const ingredientsContainer = document.querySelector('.form__field-group-ingredientes-container');
const nameIngredient = document.querySelector('#id_license_act');
const formDropdownItems = document.querySelector('.form__dropdown-items');
const cantidadVal = document.querySelector('#cantidadVal');
const cantidad = document.querySelector('#cantidad')
const addIng = document.querySelector('#addIng');

const api = new Api(apiUrl);


function Ingredients() {

    // клик по элементам с сервера
    const dropdown = (e) => {
        if (e.target.classList.contains('dropdown-item')) {
            nameIngredient.value = e.target.textContent;
            nameIngredient.date = e.target.getAttribute('data-val-date');
            nameIngredient.amount = e.target.getAttribute('data-val-amount');
            nameIngredient.distr = e.target.getAttribute('data-val-distr');
            console.log(nameIngredient.amount)
            formDropdownItems.style.display = ''
            console.log('dropdown');
            ingredients.addIngredient();
        }
    };
    // Добавление элемента из инпута
    const addIngredient = (e) => {

        if(nameIngredient.value) {
            const data = getValue();

            const elem = document.createElement('div');
            elem.id = `ing_0`;
            elem.classList.add('form__field-item-ingredient');
            document.getElementById('id_license_act').value = data.name;
            document.getElementById('id_license_date').value = data.date;
            document.getElementById('id_license_amount').value = data.amount;
            document.getElementById('id_license_amount').readOnly = true;
            document.getElementById('id_license_date').readOnly = true;
            document.getElementById('id_license_distributor').readOnly = true;
            document.getElementById('id_license_distributor').getElementsByTagName('option')[data.distr].selected = 'selected';
            elem.innerHTML = ``
            /*
            `
            <fieldset active>
            <div class="row">
                <div class="col-2">
                    <p class="text-center mb-1">Акт П/П</p>
                     <input id="valueIngredient" class="form-control text-center" name="valueIngredient"  value="${data.name}">
                </div>
                <div class="col-2">
                    <p class="text-center mb-1">Акт П/П</p>
                         <input id="valueIngredient" class="form-control text-center" name="valueIngredient"  value="${data.date}">
                </div>
                <div class="col-2">
                    <p class="text-center mb-1">Акт П/П</p>
                    <input id="valueIngredient" class="form-control text-center" name="valueIngredient"  value="${data.distr}">
                </div>
                <div class="col-2">
                    <p class="text-center mb-1">Акт П/П</p>
                    <input id="unitsIngredient" class="form-control text-center" name="unitsIngredient" value="${data.amount}">
                </div>
            </div>
            </fieldset>`*/
            console.log(elem)
            ingredientsContainer.appendChild(elem);
        }
    };
    // удаление элемента

    const eventDelete = (e) => {
        console.log('eventDelete')
        if(e.target.classList.contains('form__field-item-delete')) {
            const item = e.target.closest('.form__field-item-ingredient');
            item.removeEventListener('click',eventDelete);
            item.remove()
        };
    };
    // получение данных из инпутов для добавления
    const getValue = (e) => {
        console.log('получение данных из инпутов для добавления')
        const data = {
            name: nameIngredient.value,
            date: nameIngredient.date,
            amount: nameIngredient.amount,
            distr: nameIngredient.distr,
        };
       // clearValue(nameIngredient);
       // clearValue(cantidad);
        return data;
    };
    // очистка инпута
    const clearValue = (input) => {
        input.value = '';
    };
    return {
        clearValue,
        getValue,
        addIngredient,
        dropdown
    }
}

const cbEventInput = (elem) => {
    console.log('выпадающий список')

    return api.getLicense(elem.target.value).then( e => {
        if(e.length !== 0 ) {
            const items = e.map( elem => {
                console.log(elem.target)
                return `<li><a class="dropdown-item" id="addIng"
                    data-val-amount="${elem.amount}"
                    data-val-distr="${elem.distributor}"
                    data-val-date="${elem.date}"">${elem.act}</a></li>`

            }).join(' ')
            formDropdownItems.style.display = 'block';
            formDropdownItems.innerHTML = items;
        } else {
            const items = `<li><a class="dropdown-item" id="addIng" data-val="${elem.target.value}">${elem.target.value}</a></li>`
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
nameIngredient.addEventListener('input', eventInput);
const ingredients = Ingredients();
// вешаем слушатель на элементы с апи
formDropdownItems.addEventListener('click', ingredients.dropdown);
// вешаем слушатель на кнопку
