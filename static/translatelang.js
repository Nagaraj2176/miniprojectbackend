function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        layout: google.translate.TranslateElement.InlineLayout.HORIZONTAL,
        autoDisplay: false,
        includedLanguages: 'es,kn,en,hi,tcy', // Add languages you want to support
    }, 'google_translate_element');
}

// Load the Google Translate API script
(function() {
    var gtScript = document.createElement('script');
    gtScript.type = 'text/javascript';
    gtScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(gtScript);
})();

// (function() {
//     function adjustHeaderMargin() {
//         // Check if Google Translate iframe is present
//         const translateFrame = document.querySelector('.goog-te-banner-frame');
//         const header = document.querySelector('.fullcontainer'); // Adjust selector as needed for your header

//         if (translateFrame) {
//             header.style.marginTop = '40px';
//         } else {
//             header.style.mar ginTop = '0'; // Reset if the iframe is not present
//         }
//     }

//     // Monitor for DOM changes to detect when Google Translate becomes active
//     const observer = new MutationObserver(() => {
//         adjustHeaderMargin();
//     });

//     // Start observing the body for changes
//     observer.observe(document.body, { childList: true, subtree: true });

//     // Run initially to handle cases where the iframe is already loaded
//     adjustHeaderMargin();
// })();




// let filter_element=document.querySelector('.filter-container');

// function adjust_header()
// {
//     // console.log(translate_element);
//     header_element.classList.add('hide_googletranslate');
//     // filter_element.classList.add('adjust_filter');
// }

// function adjust_header1(){
//     header_element.classList.remove('hide_googletranslate');
//     // filter_element.classList.remove('adjust_filter');
// }
let translate_element=document.querySelector('.js_translatelang');
let header_element=document.querySelector('.fullcontainer');
let filter_element=document.querySelector('.js-filter-container');
translate_element.addEventListener('click',()=>{
    let langDropdown = document.querySelector('.goog-te-combo'); // Select the entire dropdown
    
    if (langDropdown) {
        // Listen for the 'change' event on the dropdown
        langDropdown.addEventListener('change', (event) => {

            header_element.style.top=40+'px';
            filter_element.style.top=155+'px';
             let close_element=document.querySelector('VIpgJd-ZVi9od-ORHb-OEVmcd skiptranslate');
            // console.log(close_element);
        });
    }
});



// close_element.addEventListener('click',()=>{
//     adjust_header1();
//     console.log('hello');
// });
   // let langoption=document.querySelectorAll('.goog-te-combo');
    // //console.log(langoption);

    // langoption.forEach((langop,index)=>{
    //     //console.log(langop , index);
    //     if(index!==0){
    //         let langopelem=langop;
    //         console.log(langopelem);
    //         langopelem.addEventListener('change',()=>{
    //             console.log('hrllo');
    //         })
    //     }
    // })
    // langoption.addEventListener('click',()=>{
    //     console.log();
    // })
    // langoption.forEach((langoption_elem)=>{
        // let langop=langoption_elem;
        
        // langoption.addEventListener('change',()=>{
        //     console.log('hello');
        //     // adjust_header();
        // })