$('.toast').toast('show');

const mobileBurger = $('#burger-menu-icon'); 
const mobileNav = $('.mobile-nav-side');
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
});

