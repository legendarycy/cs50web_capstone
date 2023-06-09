
//retrieve parameters from url
const urlSearchParams = new URLSearchParams(window.location.search);
let params = Object.fromEntries(urlSearchParams.entries());


//load slots function
function load_slots(button) {
    //clear seating plan and selected seats
    let sp_elem = document.querySelector('#seating-plan');
    let selected_seats_elem = document.querySelector('#selected_seats');
    selected_seats_elem.innerHTML = '';

    slot_id = parseInt(button.dataset.id);
    fetch(`/get_seats?slot_id=${slot_id}`)
    .then(response=>response.json())
    .then(data => {
        console.log(data);
        reserved_by_user = [];
        data.reserved_by_user.forEach(function(each) {
            const f_str = `${parseInt(each['seat_row'])},${parseInt(each['seat_column'])}`;
            reserved_by_user.push(f_str);
        })

        unavailable_seats = [];
        data.unavailable.forEach(function(each) {
            const f_str = `${parseInt(each['seat_row'])},${parseInt(each['seat_column'])}`;
            unavailable_seats.push(f_str);
        })

        data = data.data;
        sp_elem.innerHTML = `
        <h6>Seating Plan - Hall ${data.hall}</h6>
        <div id = 'screen-container'>
            <div id = 'screen'>screen</div>
        </div>
        `;

        for (i = 1; i <= data.rows; i++) {
            let row_elem = document.createElement('div');
            row_elem.classList.add(
                'row', 'seat-gaps', 
                'd-flex', 'justify-content-center'
            );

            let row_marker = document.createElement('div');
            row_marker.id = 'row_marker';
            row_marker.innerHTML = `<h6>${String.fromCharCode(i + 64)}</h6>`
            row_elem.append(row_marker);

            for (j = 1; j <= data.columns; j++) {
                let seat_elem = document.createElement('div');
                seat_elem.classList.add('seat');

                if (reserved_by_user.includes(`${i},${j}`)) {
                    seat_elem.classList.add('selected')
                } else if (unavailable_seats.includes(`${i},${j}`)) {
                    seat_elem.classList.add('unavailable')
                }

                seat_elem.onclick = function() {
                    seat_selection(seat_elem);
                }

                seat_elem.dataset.row = i;
                seat_elem.dataset.column = j;
                seat_elem.dataset.slot = data.id;
                if (j === data.columns/2) {
                    row_elem.append(seat_elem);
                    let blank = document.createElement('div');
                    blank.classList.add('blank');
                    row_elem.append(blank);
                } else {
                    row_elem.append(seat_elem);
                }
                
            }
            sp_elem.append(row_elem);
        }
        update_selected_seats()
    })
}


//seat selection function
function seat_selection(button) {
    fetch('/check_login')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.message) {
            const classList = button.classList;
            const classesToCheck = ['selected', 'unavailable'];
            let seat = [
                parseInt(button.dataset.row), 
                parseInt(button.dataset.column), 
                parseInt(button.dataset.slot)
              ]
            
            const containsAnyClass = classesToCheck.some(className => classList.contains(className));
            if (!containsAnyClass) {
              fetch('/reserve_seat', {
                method: 'POST',
                body: JSON.stringify(seat)
              })
              .then(response => response.json())
              .then(data => {
                if (data.message === 'Success') {
                    button.classList = 'seat selected';
                } else if (data.message === 'Conflict') {
                    button.classList = 'seat unavailable'
                }
                update_selected_seats()
              })
            } else if (button.classList.contains('selected')) {
                fetch('/reserve_seat?action=unreserve', {
                    method: 'POST',
                    body: JSON.stringify(seat)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message === 'Success') {
                        button.classList = 'seat';
                    }
                    update_selected_seats()
                })
            }
        } else {
            alert('Please login to purchase tickets')
        }

    })
}


//function to update selected seats
function update_selected_seats() {
    let selected_seats_elem = document.querySelector('#selected_seats');
    let selected_ls = [];
    document.querySelectorAll('.selected').forEach(function(each) {
        selected_ls.push(`${String.fromCharCode(parseInt(each.dataset.row)+64)}${each.dataset.column}`)
    });
    selected_seats_elem.innerHTML = (selected_ls.length > 0) ? `
    <h6>Selected</h6>
    <p>${selected_ls}<p>
    <p><b>Total:</b> S$${selected_ls.length*10}.00</p>
    <button class = 'btn btn-yellow' onclick = 'checkout()'><i class="fas fa-cart-shopping"></i> Checkout</button>
    `:'';
}


//payment function
function checkout() {
    let seats = [];
    document.querySelectorAll('.selected').forEach(function(each) {
        each.classList = 'seat unavailable';
        seats.push([
            parseInt(each.dataset.row), 
            parseInt(each.dataset.column), 
            parseInt(each.dataset.slot)
        ]);
    });
    
    fetch(`/checkout`, {
        method: 'POST',
        body: JSON.stringify(seats)
    })
    .then(response => response.json())
    .then(data => {
        let selected_seats_elem = document.querySelector('#selected_seats')
        if (data.message === 'Success') {
            selected_seats_elem.innerHTML = `
            <h6 id = 'success-prompt'>Transaction approved, enjoy your movie!</h6>
            <br>
            <img src = '${data.ticket}' class = 'qr_code'></img>
            <br>
            <p class = 'reminder'>Save this QR Code to admit all guests associated with the purchased tickets</p>
            `
        } else if (data.message === "expired"){
            selected_seats_elem.innerHTML = `
            <h6 id = 'error-prompt'>Tickets have expired, please reselect.</h6>
            `
        } else {
            selected_seats_elem.innerHTML = `
            <h6 id = 'error-prompt'>Something went wrong, please try again.</h6>
            `
        }
    })

}

document.addEventListener('DOMContentLoaded', function () {
    //submit comment
    document.querySelector('#comment-submission').addEventListener('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(this);
        formData.append('id', this.dataset.id)
        console.log(formData.get('comment'));
        console.log(formData.get('rating'));
        fetch(`post_comment`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })

        document.querySelectorAll('.star').forEach(function(each) {
            each.classList.remove('active');

        })
        location.reload()
    })

    //rating buttons
    document.querySelectorAll('.star').forEach(function(each) {
        each.addEventListener('click', function(event) {
            event.preventDefault()

            //get the value of the rating selected
            const btn = event.currentTarget;
            const rating = parseInt(btn.dataset.rating);

            //set the value of the hidden element
            const rating_given = document.querySelector('#rating-given')
            rating_given.value = rating;

            document.querySelectorAll('.star').forEach(function(each) {
                if (each.dataset.rating <= rating) {
                    each.classList.add('active')
                } else {
                    each.classList.remove('active')
                }
            })
            
        })
    })
})
