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
                if (this_val.hasClass("remove-from-cart")) {
                    // Change button to Add
                    this_val.html('<i class="fi-rs-shopping-cart mr-5"></i>Add');
                    this_val.removeClass("remove remove-from-cart").addClass("add my-add-to-cart");
                } else {
                    // Change button to Trash
                    this_val.html('<i class="fi-rs-trash mr-5" style="color: white;"></i>');
                    this_val.removeClass("add my-add-to-cart").addClass("remove remove-from-cart");
                }
                $('#cart-items-count').text(response.total_items);
                $('.new-product-added').html(response.context);
                $('.mina-total-amount').html((response.cart_total_amount).toFixed(2));
            }
        });
    });

    // Remove products from cart
    $(document).on("click", ".remove-from-cart", function () {
        var product_id = $(this).attr("data-product-id");
        var this_val = $(this);

        $.ajax({
            url: '/delete-from-cart',
            data: {
                'id': product_id,
            },
            dataType: 'json',
            beforeSend: function () {
                this_val.attr('disabled', true);
            },
            success: function (response) {
                $('.my-total-items').text(response.total_items);
                $('.mina-total-amount').text(response.cart_total_amount.toFixed(2));
                this_val.attr('disabled', false);
                $('.product-row-' + product_id).remove();

                // Change button to Add
                this_val.html('<i class="fi-rs-shopping-cart mr-5"></i>Add');
                this_val.removeClass("remove remove-from-cart").addClass("add my-add-to-cart");
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

    // add to compare
    $(".add-to-compare").on("click", function (event) {
        event.preventDefault();
        let this_val = $(this);
        let _index = this_val.attr("data-index");
        let product_id = $(".product-id-" + _index).val();
        let product_image = $(".product-image-" + _index).val();
        let product_title = $(".product-title-" + _index).val();
        let product_pid = $(".product-pid-" + _index).val();
        let product_price = $("#current-product-price-" + _index).text();
        let product_in_stock = $(".product-in-stock-" + _index).val();
        let product_description = $(".product-description-" + _index).val();

        $.ajax({
            url: '/add-to-compare',
            data: {
                'title': product_title,
                'id': product_id,
                'price': product_price,
                'pid': product_pid,
                'image': product_image,
                'in_stock': product_in_stock,
                'description': product_description,
            },
            datatype: 'json',
            success: function (response) {
                this_val.html("✔");
                $('#compare-items-count').text(response.total_items);
            }
        });
    });
    // Remove products from compare
    $(document).on("click", ".remove-from-compare", function () {
        let product_id = $(this).attr("data-product-id");
        let this_val = $(this);

        $.ajax({
            url: '/delete-from-compare',
            data: {
                'id': product_id,
            },
            dataType: 'json',
            beforeSend: function () {
                this_val.attr('disabled', true);
            },
            success: function (response) {
                $('#compare-items-count').text(response.total_items);
                $('.my-total-items').text(response.total_items);
                this_val.attr('disabled', false);
                $('.image-row-' + product_id).remove();
                $('.title-row-' + product_id).remove();
                $('.price-row-' + product_id).remove();
                $('.des-row-' + product_id).remove();
                $('.stock-row-' + product_id).remove();
                $('.add-row-' + product_id).remove();
                $('.remove-row-' + product_id).remove();
            }
        });
    });
});

let commentBodyInput = document.getElementById("comment-new")
let nameInput = document.getElementById("name-new")
let commentForm = document.getElementById("comment-form-new")
let hiddenInput = document.querySelector(".product-id-input")
const stars = document.querySelectorAll(".stars i");
let starValue = "0";
let commentList = document.querySelector(".comment-list")
stars.forEach((star, index1) => {
    star.addEventListener("click", () => {
        starValue = star.getAttribute("data-value");
        stars.forEach((star, index2) => {
            index1 >= index2 ? star.classList.add("active") : star.classList.remove("active");
        });
    });
});
if (commentForm) {
    commentForm.addEventListener("submit", function (event) {
        event.preventDefault();
        let reviewBody = commentBodyInput.value;
        let name = nameInput.value;
        let product_id = hiddenInput.value;
        let formDiv = document.querySelector(".comment-form-div")
        let afterAdd = document.getElementById("review-res")

        $.ajax({
            type: 'POST',
            url: '/add-new-review/',
            data: {
                'review_body': reviewBody,
                'name': name,
                'product_id': product_id,
                'rating_value': starValue,
            },
            datatype: 'json',
            success: function (response) {
                if (response.boolean === 'true') {
                    formDiv.style.display = 'none'
                    afterAdd.style.display = "block";
                    afterAdd.innerHTML = "Thanks for your review. It added successfully!"
                    setTimeout(function () {
                        afterAdd.style.display = 'none'
                    }, 4000)
                }
            }
        })
    })
}

let replyBtns = document.querySelectorAll(".reply")

replyBtns.forEach(function (btn) {
    btn.addEventListener("click", function (event) {
        event.preventDefault();
        let parentElement = btn.closest(".reply-parent");
        let replyFormDiv = parentElement.querySelector(".reply-form-div")
        if (replyFormDiv.style.display === 'none' || replyFormDiv.style.display === '') {
            replyFormDiv.style.display = 'block';
        } else {
            replyFormDiv.style.display = 'none';
        }
        let replyForm = replyFormDiv.querySelector('.reply_form')
        let replyBodyInput = replyFormDiv.querySelector(".reply-new")
        let replyHiddenInput = replyFormDiv.querySelector(".reply-product-id-input")
        let parentIdInput = replyFormDiv.querySelector(".parent-id")

        replyForm.addEventListener("submit", function (event) {
            event.preventDefault();
            let reviewBody = replyBodyInput.value;
            let product_id = replyHiddenInput.value;
            let formDiv = replyFormDiv;
            let afterAdd = parentElement.querySelector(".review-res-reply")
            let parentId = parentIdInput.value;

            $.ajax({
                type: 'POST',
                url: '/add-new-reply/',
                data: {
                    'review_body': reviewBody,
                    'product_id': product_id,
                    'parent_id': parentId,
                },
                datatype: 'json',
                success: function (response) {
                    if (response.boolean === 'true') {
                        formDiv.style.display = 'none'
                        afterAdd.style.display = "block";
                        afterAdd.textContent = "Thanks for your reply. It added successfully!"
                        setTimeout(function () {
                            afterAdd.style.display = 'none'
                        }, 4000)
                    }
                }
            })
        })

    });
});