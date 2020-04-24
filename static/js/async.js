$(document).ready(function(){
    //ContactForm
    var contactForm = $('.contact-form');
    var contactFormMethod = contactForm.attr('method');
    var contactFormEndpoint = contactForm.attr('action');
    function displaySubmit(sb,dt,s){
      if(s){
        sb.addClass("disabled")
        sb.html("<i class='fa fa-spin fa-'></i> Sending...")
      }else{
        sb.removeClass("disabled")
        sb.html(dt)
      }
    }
    contactForm.submit(function(event){
      event.preventDefault()
      var contactBtn = contactForm.find("[type='submit']");
      var contactFormData = contactForm.serialize();
      var thisForm = $(this);
      displaySubmit(contactBtn,"",true)
      $.ajax({
        method:contactFormMethod,
        url:contactFormEndpoint,
        data:contactFormData,
        success:function(data){
          contactForm[0].reset()
          $.alert({
            title:"Success!",
            content:data.message,
            theme:"modern",
          })
          setTimeout(function(){
            displaySubmit(contactBtn,"Submit",false)
          },500)
        },
        error:function(error){
          var jsonData = error.responseJSON;
          var msg = "";
          $.each(jsonData,function(key,value){
            msg+= key + ":" + value[0].message + "<br/>"
          })
          $.alert({
            title:"Error",
            content:msg,
            theme:"modern",
          })
          setTimeout(function(){
            displaySubmit(contactBtn,"Submit",false)
          },500)
        }
      })
    })

    //AutoSearch
    var searchForm = $('.search-form')
    var searchInput = searchForm.find("[name='q']")
    var searchBtn = searchForm.find("[type='submit']")
    var typingTimer;
    var typingInterval = 500;

    searchInput.keyup(function(event){
      clearInterval(typingTimer)
      typingTimer = setTimeout(performSearch,typingInterval)
    })

    searchInput.keydown(function(event){
      clearInterval(typingTimer)
    })

    function showSearch(){
      searchBtn.addClass("disabled")
      searchBtn.html("<i class='fa fa-spin fa-'></i> Searching...")
    }

    function performSearch(){
      showSearch()
      var query=searchInput.val()
      setTimeout(function(){
        window.location.href='/search/?q='+query
      },1000)    
    }

    //ProductForm 
    var productForm = $('.form-product-async')
    productForm.submit(function(event){
      event.preventDefault()
      var thisForm = $(this);
      var actionEndpoint = thisForm.attr('action');
      var httpMethod = thisForm.attr('method');
      var formData = thisForm.serialize();

      $.ajax({
        url:actionEndpoint,
        method:httpMethod,
        data:formData,
        success:function(data){
        var submitSpan = thisForm.find(".submit-span")
        if(data.added){
          submitSpan.html("<h5>In Cart -<button class='btn btn-link mb-1'>Remove?</button></h5>")
        }else{
          submitSpan.html("<button class='btn btn-success'>Add to Cart</button>")
        }
        var navBarCount = $('.nav-cart-count');
        navBarCount.text(data.count)
        },
        error:function(errorData){
          $.alert("An Error Occured!")
          console.log("error",errorData)
        }
      })
    })
  })