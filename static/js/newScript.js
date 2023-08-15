$(document).ready(() => {
    // Get references to the elements
    const btnUploadImage = document.getElementById("btnUploadImage");
    const hiddenInput = document.getElementById("hidden-input");
    const loadImage = document.getElementById("load-image");
    const clearButton = document.getElementById("clear");
    const formImageUpload = document.getElementById("form-image-upload");
    const mamdaniImage = document.getElementById("combined-image-mamdani");
    const sugenoImage = document.getElementById("combined-image-sugeno");
    const tsukamotoImage = document.getElementById("combined-image-tsukamoto");

    function showLoadingOverlay() {
        document.getElementById('loading-overlay').classList.remove('hidden');
    }

    function hideLoadingOverlay() {
        document.getElementById('loading-overlay').classList.add('hidden');
    }

    // Add event listener to the btnUploadImage button
    btnUploadImage.addEventListener("click", function () {
        hiddenInput.click(); // Trigger the click on the hidden input element
    });

    // Listen for changes in the file input
    hiddenInput.addEventListener("change", function (event) {
        const file = event.target.files[0]; // Get the selected file (first file if multiple allowed)

        // Check if a file is selected
        if (file) {
            const reader = new FileReader();

            // Read the file as a data URL and set the src attribute of the loadImage element
            reader.addEventListener("load", function () {
                loadImage.src = reader.result;
            });

            reader.readAsDataURL(file); // Read the file as data URL

            // Display the file name and size in the loadImage element
            loadImage.alt = file.name; // Set the alt attribute to the file name
            loadImage.title = `File Name: ${file.name}\nFile Size: ${formatFileSize(file.size)}`; // Set the title attribute to include file name and size
        }

        $('#btnEnhancement').removeClass('hidden')
        $('#btnUploadImage').addClass('hidden')
    });

    // Helper function to format file size
    function formatFileSize(size) {
        const units = ['B', 'KB', 'MB', 'GB'];
        let index = 0;
        while (size >= 1024 && index < units.length - 1) {
            size /= 1024;
            index++;
        }
        return `${size.toFixed(2)} ${units[index]}`;
    }

    // Add event listener to the "Clear" button
    // clearButton.addEventListener("click", function () {
    //     loadImage.src = "https://via.placeholder.com/290x373" // Reset the src attribute to clear the image
    //     mamdaniImage.src = "https://via.placeholder.com/224x288"
    //     sugenoImage.src = "https://via.placeholder.com/224x288"
    //     tsukamotoImage.src = "https://via.placeholder.com/224x288"
    //     // mamdaniImage.removeAttribute("src");
    //     // sugenoImage.removeAttribute("src");
    //     // tsukamotoImage.removeAttribute("src");
    //     loadImage.alt = ""; // Clear the alt attribute
    //     loadImage.title = ""; // Clear the title attribute
    //     $('#btnUploadImage').removeClass('hidden')
    //     $('#btnEnhancement').addClass('hidden')
    //     $('#btnInformation').addClass('hidden')
    //     $('#btnCalculate').addClass('hidden')
    // });

    document.getElementById("clear").onclick = (event) => {
        event.preventDefault(); // Prevent the default form submission

        loadImage.src = "https://via.placeholder.com/290x373" // Reset the src attribute to clear the image
        loadImage.alt = ""; // Clear the alt attribute
        loadImage.title = ""; // Clear the title attribute

        // Clear the file input value
        document.getElementById("hidden-input").value = null;

        $('#card-image-enhancement').addClass('hidden');
        $('.image-enhancement').empty();
        $('#btnUploadImage').removeClass('hidden')
        $('#btnEnhancement').addClass('hidden')
        $('#btnInformation').addClass('hidden')
        $('#btnCalculate').addClass('hidden')
        $('.pnsr').addClass('hidden')
    };

    // Handle the form submission
    formImageUpload.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent the default form submission
        showLoadingOverlay(); // Show the loading overlay when the form is submitted

        // Create a new FormData object and append the file input data
        var formData = new FormData();
        formData.append("file-image", hiddenInput.files[0]);

        $.ajax({
            url: "/process_image",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                // Hide the loading overlay when the form processing is completed
                hideLoadingOverlay();

                // The rest of your code to handle the response
                // Enhancement
                const histogramEnhancement = response.histogram_enhancement
                const mamdaniEnhancement = response.mamdani_enhancement;
                const sugenoEnhancement = response.sugeno_enhancement
                const tsukamotoEnhancement = response.tsukamoto_enhancement

                // Clahe
                const claheEnhancement = response.clahe_enhancement

                // Combine Enhancement
                const histogramCombined = response.histogram_encoded_image
                const mamdaniCombined = response.encoded_image;
                const sugenoCombined = response.sugeno_encoded_image
                const tsukamotoCombined = response.tsukamoto_encoded_image

                // alert(enhanced, sugenoEnhanced, tsukamotoEnhanced, histogramEnhanced);
                console.log(response.clahe_pnsr);
                // console.log(response.combine_mamdani_pnsr);
                // console.log(response.combine_sugeno_pnsr);
                // console.log(response.combine_tsukamoto_pnsr);

                $('#card-image-enhancement').removeClass('hidden');

                $('#combined-image-mamdani').attr("src", mamdaniCombined);
                $('#combined-image-sugeno').attr("src", sugenoCombined);
                $('#combined-image-tsukamoto').attr("src", tsukamotoCombined);

                $('.combined-histogram-pnsr').text(response.combine_histogram_pnsr.toFixed(4))
                $('.combined-mamdani-pnsr').text(response.combine_mamdani_pnsr.toFixed(4))
                $('.combined-sugeno-pnsr').text(response.combine_sugeno_pnsr.toFixed(4))
                $('.combined-tsukamoto-pnsr').text(response.combine_tsukamoto_pnsr.toFixed(4))
                $('.value-pnsr-clahe').text(response.clahe_pnsr.toFixed(4))
                $('.value-pnsr-histogram').text(response.histogram_pnsr.toFixed(4))
                $('.value-pnsr-mamdani').text(response.mamdani_pnsr.toFixed(4))
                $('.value-pnsr-sugeno').text(response.sugeno_pnsr.toFixed(4))
                $('.value-pnsr-tsukamoto').text(response.tsukamoto_pnsr.toFixed(4))

                $('.image-clahe').attr("src", claheEnhancement);
                $('#image-histogram').attr("src", histogramEnhancement);
                $('#image-mamdani').attr("src", mamdaniEnhancement);
                $('#image-sugeno').attr("src", sugenoEnhancement);
                $('#image-tsukamoto').attr("src", tsukamotoEnhancement);
                $('#image-combine-histogram').attr("src", histogramCombined);
                $('#image-combine-sugeno').attr("src", sugenoCombined);
                $('#image-combine-mamdani').attr("src", mamdaniCombined);
                $('#image-combine-tsukamoto').attr("src", tsukamotoCombined);

                $('#btnCalculate').removeClass('hidden')
                $('#btnCalculate').removeClass('hidden')
                $('#btnEnhancement').addClass('hidden')
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });

    document.getElementById("btnCalculate").onclick = (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Calculate PNSR
        $('.value-pnsr').removeClass('hidden')
        $('#btnInformation').removeClass('hidden')
    }

    // Disable going back using browser history
    history.pushState(null, null, location.href);
    window.onpopstate = function (event) {
        history.go(1);
    };
    
})