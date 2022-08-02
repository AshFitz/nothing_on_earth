$('.toast').toast('show');

const mobileBurger = $('#burger-menu-icon'); 
const mobileNav = $('.mobile-nav-side');
const deleteButton = $('#delete-button');
const closeButton = $('#close-product-button');
const deletePopup = $('.overlay-delete');
const popupText = $('#delete-popup');  
const navBackground = $('.nav-background');

mobileBurger.click(function(){
    navBackground.show();
    navBackground.addClass('overlay-nav');
    mobileNav.addClass('transition-right');
    return false;
});


navBackground.click(function(){
    navBackground.removeClass('overlay-nav');
    mobileNav.removeClass('transition-right');
    navBackground.css("display", "none")
});

deleteButton.click(function(){
    deletePopup.show();
    popupText.show();
    return false;
});

closeButton.click(function(){
    deletePopup.hide();
    popupText.hide();
})

deletePopup.click(function(){
    deletePopup.hide();
    popupText.hide();
});

