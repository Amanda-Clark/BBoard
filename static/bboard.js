    function display_c(){
            var refresh=1000; // Refresh rate in milli seconds
            mytime=setTimeout('display_ct()',refresh)
        }
        function display_ct() {
            var x = new Date()
            document.getElementById('ct').innerHTML = x;
            display_c();
        }
       var slideIndex = 1;


       showSlides(slideIndex);

        function plusSlides(n) {
            showSlides(slideIndex += n);
        }

        function currentSlide(n) {
            showSlides(slideIndex = n);
        }

        function showSlides(n) {
            var i;
            var slides = document.getElementsByClassName("news");
            var slides2 = document.getElementsByClassName("ornews");

            if (n > slides.length) {slideIndex = 1}
            if (n < 1) {slideIndex = slides.length}
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }

            slides[slideIndex-1].style.display = "block";

            if (n > slides2.length) {slideIndex = 1}
            if (n < 1) {slideIndex = slides2.length}
            for (i = 0; i < slides2.length; i++) {
                slides2[i].style.display = "none";
            }

            slides2[slideIndex-1].style.display = "block";

        }
        function cyclenews(){
            plusSlides(1)
            news_timeout();
        }
        function news_timeout(){
            var refresh=15000; // Refresh rate in milli seconds
            mytime=setTimeout('cyclenews()',refresh)
        }
        function timedRefresh(timeoutPeriod) {
	        setTimeout("location.reload(true);",timeoutPeriod);
        }