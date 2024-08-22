//console.log("Working")
//
//$("#commentForm").submit(function(e){
//    e.preventDefault();
//
//    $.ajax({
//        data: $(this).serialize(),
//
//        method: $(this).attr("method"),
//
//        url: $(this).attr("action"),
//
//        datatype: "json",
//
//        success: function(res){
//            console.log("Comment Saved to DB...");
//
//            if(res.bool == true){
//                $("#review-res").html("Review added successfully.")
//            }
//        }
//    })
//})

console.log("Working");

$("#commentForm").submit(function(e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",

        success: function(res) {
            console.log("Comment Saved to DB...");

            // Check the response in the console
            console.log(res);

            if (res.bool === true) {
                $("#review-res").html("Review added successfully.");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">';
                _html += '<div class="user justify-content-between d-flex">';
                _html += '<div class="thumb text-center">';
                _html += '<img src="{% static "assets/imgs/blog/author-2.png" %}" alt="" />';
                _html += '<a href="#" class="font-heading text-brand">' + res.context.user + '</a>';
                _html += '</div>';

                _html += '<div class="desc">';
                _html += '<div class="d-flex justify-content-between mb-10">';
                _html += '<div class="d-flex align-items-center">';
                _html += '<span class="font-xs text-muted">' + new Date().toLocaleDateString() + '</span>'; // Fixed date
                _html += '</div>';

                for (let i = 1; i <= res.context.rating; i++) { // Ensure correct rating logic
                    _html += '<i class="fas fa-star text-warning"></i>';
                }

                _html += '</div>';
                _html += '<p class="mb-10">' + res.context.review + '</p>';

                _html += '</div>';
                _html += '</div>';
                _html += '</div>';

                $(".comment-list").prepend(_html);
            } else {
                $("#review-res").html("Failed to add review.");
            }
        },
        error: function(xhr, status, error) {
            console.log("Error: " + error);
            $("#review-res").html("An error occurred. Please try again.");
        }
    });
});


$(document).ready(function (){
    $(".filter-checkbox , #price-filter-btn").on("click", function(){
        console.log("A checkbox have been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price
        filter_object.max_price = max_price

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + "]:checked")).map(function(element){
                return element.value
            })
        })
        console.log("Filter object is:", filter_object);
        $.ajax({
            url: '/filter_product',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Trying to filter product...");
            },
            success: function(response){
                console.log(response);
                console.log("Data Filtered sucessfully")
                $("#filtered-product").html(response.data)
            }
        })
    })

     $("#max_price").on('blur', function(){
        let min_price = parseFloat($(this).attr("min"));
        let max_price = parseFloat($(this).attr("max"));
        let current_price = parseFloat($(this).val());

        console.log("Min", min_price);
        console.log("Max", max_price);
        console.log("Current", current_price);

        if (current_price < min_price || current_price > max_price) {
            console.log("Price error occurred");

            let min_Price = Math.round(min_price * 100) / 100;
            let max_Price = Math.round(max_price * 100) / 100;

            console.log("Min Price", min_Price);
            console.log("Max Price", max_Price);

            alert("Price must be between: " + min_Price + " and " + max_Price);
            $(this).val(min_price);
            $("#range").val(min_price);

            $(this).focus();
            return false;
        }
    })

        $(".add-to-cart-btn").on("click",function(){
        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()

        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()

        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()

        console.log("Quantity:", quantity);
        console.log("Title:", product_title);
        console.log("Price:", product_price);
        console.log("ID:", product_id);
        console.log("PID:", product_pid);
        console.log("Image:", product_image);
        console.log("Index:", index);
        console.log("Current Element:", this_val);


        $.ajax({
            url: '/add-to-cart',
            data: {
                'id' : product_id,
                'pid' : product_pid,
                'image': product_image,
                'qty' : quantity,
                'title' : product_title,
                'price': product_price,
            },
            dataType : 'json',
            beforeSend: function(){
                console.log("Adding product to cart....");
            },
            success: function(response){
            this_val.html("✓")
                console.log("Added to cart!")
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })


   $(".delete-product").on("click", function(){
            let product_id = $(this).attr("data-product");
            let this_val = $(this);

            console.log("Product ID:", product_id);

            $.ajax({
                url:"/delete-from-cart",
                data: {
                    "id":product_id
                },
                dataType: "json",
                beforeSend: function(){
                    this_val.hide();
                },
                success: function(response){
                    this_val.show()
                    $(".cart-items-count").text(response.totalcartitems)
                    $("#cart-list").html(response.data)
                }
            })

        });


   $(".update-product").on("click", function(){
            let product_id = $(this).attr("data-product");
            let this_val = $(this);
            let product_qty = $(".product-qty-"+product_id).val()

            console.log("Product ID:", product_id);
            console.log("Product Qty:", product_qty);

            $.ajax({
                url:"/update-cart",
                data: {
                    "id":product_id,
                    "qty": product_qty
                },
                dataType: "json",
                beforeSend: function(){
                    this_val.hide();
                },
                success: function(response){
                    this_val.show()
                    $(".cart-items-count").text(response.totalcartitems)
                    $("#cart-list").html(response.data)
                }
            })

        });

        // Making Default Address
        $(document).on("click", ".make-default-address", function(){
            let id = $(this).attr("data-address-id")
            let this_val = $(this)

            console.log("ID is:", id);
            console.log("Element is:", this_val);

            $.ajax({
                url:"/make-default-address",
                data: {
                    "id":id
                },
                dataType: "json",
                success: function(response){
                    console.log("Address made default...");
                    if (response.boolean == true){
                        $(".check").hide()
                        $(".action-btn").show()

                        $(".check"+id).show()
                        $(".button"+id).hide()
                    }
                }
            })
        })
})



console.log("Done");