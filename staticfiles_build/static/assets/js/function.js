const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dev"];


$(document).ready(function () {
    // New comment
    $("#commentForm").submit(function (e) {
        e.preventDefault();

        let dt = new Date();
        let time = monthNames[dt.getUTCMonth()] + " " + dt.getDate() + ", " + dt.getFullYear()

        $.ajax({
            data: $(this).serialize(),
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            datatype: "json",
            success: function (res) {

                if (res.bool === true) {
                    $("#review-res").html("Review added successfully.")
                    setTimeout(() => {
                        $("#review-res").hide();
                    }, 3000)
                    $("#add-review").hide();

                    let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLsVeRshntRdpPcgbLmfHG3u1tcF8w0MFV9w&usqp=CAU" alt=""/>'
                    _html += '<a href="#" class="font-heading text-brand">' + res.context.user + '</a>'
                    _html += '</div>'

                    _html += '<div class="desc">'
                    _html += '<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">' + time + '</span>'
                    _html += '</div>'

                    for (let i = 1; i <= res.context.rating; i++) {
                        _html += '<i class="fas fa-star text-warning"></i>';
                    }

                    _html += '</div>'
                    _html += '<p class="mb-10">' + res.context.review + '</p>'
                    _html += '</div>'

                    _html += '</div>'
                    _html += '</div>'

                    $(".comment-list").prepend(_html);
                }
            }
        });
    });
    // Filter products
    $(".filter-checkbox, #filter-price-btn").on("click", function () {
        let filter_object = {}
        let min_price = $('#frommSlider').val()
        let max_price = $('#tooSlider').val()
        filter_object.min_price = min_price;
        filter_object.max_price = max_price;
        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") // category, vendor, tag
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter = ' + filter_key + ']:checked')).map(function (element) {
                return element.value
            })
        })
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            datatype: 'json',
            success: function (response) {
                $('#filtered-product').html(response.data)
                $('#product-count').hide()
            }
        });
    });
    // Add to cart
    $(".my-add-to-cart").on("click", function (event) {
        event.preventDefault();
        let this_val = $(this);
        let _index = this_val.attr("data-index");
        let product_quantity = $(".product-quantity-" + _index).val();
        let product_id = $(".product-id-" + _index).val();
        let product_title = $(".product-title-" + _index).val();
        let product_pid = $(".product-pid-" + _index).val();
        let product_image = $(".product-image-" + _index).val();
        let product_price = $("#current-product-price-" + _index).text();

        $.ajax({
            url: '/add-to-cart',
            data: {
                'title': product_title,
                'quantity': product_quantity,
                'id': product_id,
                'price': product_price,
                'pid': product_pid,
                'image': product_image,
            },
            datatype: 'json',
            success: function (response) {
                this_val.html("✔")
                $('#cart-items-count').text(response.total_items);
                $('.new-product-added').html(response.context);
                $('.mina-total-amount').html((response.cart_total_amount).toFixed(2));
                // this_val.attr('disabled', false);
            }
        });
    });
    // Remove products from cart
    $(".remove-from-cart").on("click", function remove(id) {
        id.preventDefault();
        let product_id = $(this).attr("data-product-id");
        let this_val = $(this);
        // let token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/delete-from-cart',
            data: {
                'id': product_id,
                // csrfmiddlewaretoken: token,
            },
            datatype: 'json',
            beforeSend: function () {
                this_val.attr('disabled', true);
            },
            success: function (response) {
                $('.my-total-items').html(response.total_items);
                $('.mina-total-amount').html((response.cart_total_amount).toFixed(2));
                this_val.attr('disabled', false);
                $('.product-row-' + product_id).remove();
            }
        });
    });
    // Updating quantity in cart page
    $(".update-cart").on("click", function () {
        let product_id = $(this).attr("data-product-id");
        let product_quantity = $('.product-quantity-' + product_id).val();
        let product_price = $('.my-product-price-' + product_id).text();
        let product_subtotal = product_price * product_quantity;
        let this_val = $(this);
        // let token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: '/update-cart',
            data: {
                'id': product_id,
                'quantity': product_quantity,
                // csrfmiddlewaretoken: token,
            },
            datatype: 'json',
            beforeSend: function () {
                this_val.attr('disabled', true);
            },
            success: function (response) {
                $('.mina-total-amount').html((response.cart_total_amount).toFixed(2));
                $('.product-subtotal-' + product_id).html(product_subtotal.toFixed(2));
                $('.new-product-quantity-' + product_id).html(response.product_quantity);
                this_val.attr('disabled', false);
            }
        });
    });
    // Make default address
    $('.make-default-btn').on("click", function (e) {
        e.preventDefault();
        let this_val = $(this)
        let address_id = $(this).attr('data-address-id');

        $.ajax({
            url: '/make-default-address',
            data: {
                'id': address_id,
            },
            datatype: 'json',
            success: function (response) {
                if (response.Boolean === true) {
                    $('.check').hide();
                    $('.action-btn').show();
                    $('.check' + address_id).show();
                    $('.btn' + address_id).hide();
                }
            }
        });
    });

    // Add to wishlist
    $('.add-to-wishlist').on('click', function () {
        let product_id = $(this).attr('data-product-id');
        let this_val = $(this)

        $.ajax({
            url: '/add-to-wishlist',
            data: {
                'id': product_id,
            },
            dataType: 'json',
            beforeSend: function () {
                this_val.html("✔")
            },
            success: function (response) {
                if (response.boolean === true) {
                    $('.wishlist-items').html(response.wishlist);
                }
            }
        });
    });

    // Remove from wishlist
    $('.remove-from-wishlist').on('click', function () {
        let wishlist_id = $(this).attr('data-wishlist-id')
        let this_val = $(this)

        $.ajax({
            url: '/remove-from-wishlist',
            data: {
                'id': wishlist_id,
            },
            datatype: 'json',
            beforeSend: function () {
                this_val.attr('disabled', true);
            },
            success: function (response) {
                if (response.boolean === true) {
                    $('.wishlist-items').html(response.wishlist);
                    this_val.attr('disabled', false);
                    $('.product-row-' + wishlist_id).remove();
                }
            }
        });
    });

    // Add contact us message
    $('#contact-us-form').on('submit', function (e) {
        e.preventDefault();
        let fullName = $('#full-name').val();
        let email = $('#email').val();
        let phone = $('#phone').val();
        let subject = $('#subject').val();
        let message = $('#message').val();

        $.ajax({
            url: '/contact-us-ajax',
            data: {
                'full_name': fullName,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
            },
            datatype: 'json',
            beforeSend: function () {
                console.log('sending...');
            },
            success: function (response) {
                if (response.boolean === true) {
                    $('.hide-contact-form').hide();
                    $('.message-sent').html('Message sent successfully.')
                }
            }
        });
    });
});


