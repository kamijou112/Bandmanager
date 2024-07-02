function add_cart(item_id) {
    $.get('/add_cart/' + item_id, function (response) {
        let validationMessages = $("#validation-messages");

        console.log(response);
        if (response.msg === 'Added successfully') {
            validationMessages.empty();
            validationMessages.append("<p>" + 'Add to Cart successful' + "</p>");
            validationMessages.show();

        } else {
            validationMessages.empty();
            validationMessages.append("<p>" + 'Please login first' + "</p>");
            validationMessages.show();
            window.location.href = '/login';
        }
    });
}


function calcTotal() {
    let totalPrice = 0;
    $('input[name="item_ids"]:checked').each(function () {
        let price = parseFloat($(this).closest('tr').find('td:eq(2)').text());
        let quantity = parseInt($(this).closest('tr').find('input[name="item_quantities"]').val());
        let mini_total_price = price * quantity;
        totalPrice += price * quantity;

    });
    $('#totalPrice').text(totalPrice.toFixed(2));
}

function calcTotal2(itemId) {
    let price = parseFloat($('#price' + itemId).text());
    let quantity = parseInt($('#number' + itemId).val());
    let mini_total_price = price * quantity;
    $('#total' + itemId).text(mini_total_price.toFixed(2));
    updateCart(itemId, price, quantity);
    calcTotal();
}

function updateCart(item_id, price, quantity) {
    $.ajax({
        url: '/update_cart', type: 'POST', data: {
            'item_id': item_id, 'price': price, 'quantity': quantity,
        }, success: function (data) {
            console.log(data);
        }, error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}


function like(item_id) {
    $.get('/like/' + item_id, function (response) {
        if (response.status = 'success') {
            let likeButton = $('#like_button');
            let buttonText = likeButton.text();
            let trimmedText = buttonText.trim();
            likeButton.text(trimmedText);
            if (likeButton.text() === 'Like') {
                likeButton.text('Unlike');
            } else {
                likeButton.text('Like');
            }

        } else {
            window.location.href = '/login';
        }


    });
}