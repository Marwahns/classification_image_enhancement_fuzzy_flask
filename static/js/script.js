$(document).ready(() => {
    const fileTempl = document.getElementById("file-template"),
        imageTempl = document.getElementById("image-template"),
        empty = document.getElementById("empty");

    // use to store pre selected files
    let FILES = {};

    // check if file is of type image and prepend the initialized
    // template to the target element
    function addFile(target, file) {
        const isImage = file.type.match("image.*"),
            objectURL = URL.createObjectURL(file);

        const clone = isImage
            ? imageTempl.content.cloneNode(true)
            : fileTempl.content.cloneNode(true);

        clone.querySelector("h1").textContent = file.name;
        clone.querySelector("li").id = objectURL;
        clone.querySelector(".delete").dataset.target = objectURL;
        clone.querySelector(".size").textContent =
            file.size > 1024
                ? file.size > 1048576
                    ? Math.round(file.size / 1048576) + "mb"
                    : Math.round(file.size / 1024) + "kb"
                : file.size + "b";

        isImage &&
            Object.assign(clone.querySelector("img"), {
                src: objectURL,
                alt: file.name
            });

        empty.classList.add("hidden");
        target.prepend(clone);

        FILES[objectURL] = file;
    }

    const gallery = document.getElementById("gallery"),
        overlay = document.getElementById("overlay");


    // const hidden = document.getElementById("hidden-input");
    // hidden.onchange = (e) => {
    //     for (const file of e.target.files) {
    //         addFile(gallery, file);
    //     }
    // };
    // document.getElementById("button").onclick = () => hidden.click();

    const hidden = document.getElementById("hidden-input");
    hidden.onchange = (e) => {
        for (const file of e.target.files) {
            const fileName = file.name;
            const fileExt = fileName.split('.').pop().toLowerCase();
            // alert(fileExt)

            if (fileExt === 'dcm') {
                // Trigger the /convert_dcm endpoint for DCM file
                convertDCM(file);
            } else {
                // Add non-DCM files to the gallery
                addFile(gallery, file);
            }
        }
    };

    document.getElementById("button").onclick = () => hidden.click();

    // After setting the encoded_image value
    // const imageUrl = "data:image/jpeg;base64," + encoded_image;
    // const imgPreview = clone.querySelector(".img-preview");
    // imgPreview.src = imageUrl;
    // imgPreview.alt = file.name;

    function convertDCM(file) {
        const formData = new FormData();
        formData.append('file-image', file);

        $.ajax({
            url: '/convert_dcm',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                const encodedImage = response.encoded_image;

                // Decode the base64-encoded image data
                const byteCharacters = atob(encodedImage);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);

                // Create a new Blob object from the decoded image data
                const blob = new Blob([byteArray], { type: 'image/jpeg' });

                // Create a new File object from the Blob
                const convertedFile = new File([blob], file.name, { type: 'image/jpeg' });

                // Add the converted file to the gallery
                addFile(gallery, convertedFile);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    }

    // use to check if a file is being dragged
    const hasFiles = ({ dataTransfer: { types = [] } }) =>
        types.indexOf("Files") > -1;

    // use to drag dragenter and dragleave events.
    // this is to know if the outermost parent is dragged over
    // without issues due to drag events on its children
    let counter = 0;

    // reset counter and append file to gallery when file is dropped
    function dropHandler(ev) {
        ev.preventDefault();
        for (const file of ev.dataTransfer.files) {
            addFile(gallery, file);
            overlay.classList.remove("draggedover");
            counter = 0;
        }
    }

    // only react to actual files being dragged
    function dragEnterHandler(e) {
        e.preventDefault();
        if (!hasFiles(e)) {
            return;
        }
        ++counter && overlay.classList.add("draggedover");
    }

    function dragLeaveHandler(e) {
        1 > --counter && overlay.classList.remove("draggedover");
    }

    function dragOverHandler(e) {
        if (hasFiles(e)) {
            e.preventDefault();
        }
    }

    // event delegation to capture delete events
    // from the waste buckets in the file preview cards
    gallery.onclick = ({ target }) => {
        if (target.classList.contains("delete")) {
            const ou = target.dataset.target;
            document.getElementById(ou).remove(ou);
            gallery.children.length === 1 && empty.classList.remove("hidden");
            delete FILES[ou];
        }
    };

    // alert(document.getElementById("pneumonia-percentage").text == null)
    // if (document.getElementById("gallery").value == null) {
    //     $('#submit').prop('disabled', true);
    // }

    document.getElementById("submit").onclick = (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Perform AJAX request to the server
        $.ajax({
            url: "/",
            type: "POST",
            data: new FormData(document.getElementById("form-image-upload")),
            processData: false,
            contentType: false,
            success: function (response) {
                // Successful AJAX response
                const pneumoniaPercentage = response.pneumonia_percentage;
                const formattedPercentage = (pneumoniaPercentage * 100).toFixed(2) + '%';

                // Display the "pneumonia_percentage" value in an element with ID "pneumonia-percentage"
                // document.getElementById("pneumonia-percentage").textContent = pneumoniaPercentage;
                // alert(pneumoniaPercentage)
                $('#pneumonia-percentage').text(formattedPercentage)
                $('#submit').addClass('hidden')
                $('#image-identify').removeClass("hidden")
                $('#enhancement').removeClass("hidden")
            },
            error: function (xhr, status, error) {
                // AJAX request error handling
                console.log(error);
            },
        });

    };

    // Handle the form submission
    $("form").submit(function (e) {
        e.preventDefault();  // Prevent the default form submission

        // Create a new FormData object and append the file input data
        var formData = new FormData();
        formData.append("file-image", $("input[type='file']")[0].files[0]);

        $.ajax({
            url: "/process_image",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                // Enhancement
                const histogramEnhancement = response.histogram_enhancement
                const mamdaniEnhancement = response.mamdani_enhancement;
                const sugenoEnhancement = response.sugeno_enhancement
                const tsukamotoEnhancement = response.tsukamoto_enhancement

                // Combine Enhancement
                const histogramCombined = response.histogram_encoded_image
                const mamdaniCombined = response.encoded_image;
                const sugenoCombined = response.sugeno_encoded_image
                const tsukamotoCombined = response.tsukamoto_encoded_image

                // alert(enhanced, sugenoEnhanced, tsukamotoEnhanced, histogramEnhanced);
                console.log(histogramCombined, mamdaniCombined, sugenoCombined, tsukamotoCombined);

                // Display the enhanced image 
                // const imageUrl = "data:image/png;base64," + enhanced;

                $("#image-histogram").html("<div class='flex flex-col items-center justify-center h-full'><span class='text-small text-gray-500'>Histogram Equalization</span><img src='" + histogramEnhancement + "' width='300' height='400'></div>");

                $("#image-mamdani").html("<div class='flex flex-col items-center justify-center h-full'><span class='text-small text-gray-500'>Fuzzy Mamdani</span><img src='" + mamdaniEnhancement + "' width='300' height='400'></div>");

                $("#image-sugeno").html("<div class='flex flex-col items-center justify-center h-full'><span class='text-small text-gray-500'>Fuzzy Sugeno</span><img src='" + sugenoEnhancement + "' width='300' height='400'></div>");

                $("#image-tsukamoto").html("<div class='flex flex-col items-center justify-center h-full'><span class='text-small text-gray-500'>Fuzzy Tsukamoto</span><img src='" + tsukamotoEnhancement + "' width='300' height='400'></div>");

                $("#image-container-histogram").html("<div class='flex flex-col items-center justify-center h-full'><span class='text-small text-gray-500'>Histogram Equalization</span><img src='" + histogramCombined + "' width='300' height='400'></div>");

                $("#image-container").html("<div class='flex flex-col items-center justify-center h-full'><span class='text-small text-gray-500'>Fuzzy Mamdani</span><img src='" + mamdaniCombined + "' width='300' height='400'></div>");

                $("#image-container-sugeno").html("<div class='flex flex-col items-center justify-center h-full'><span class='text-small text-gray-500'>Fuzzy Sugeno</span><img src='" + sugenoCombined + "' width='300' height='400'></div>");

                $("#image-container-tsukamoto").html("<div class='flex flex-col items-center justify-center h-full'><span class='text-small text-gray-500'>Fuzzy Tsukamoto</span><img src='" + tsukamotoCombined + "' width='300' height='400'></div>");

                // Calculate PNSR
                // $("#pnsr-container-histogram").html("<div class='block flex-col items-center h-full'><span class='text-small text-gray-500'>PNSR Histogram Equalization Enhancement</span>'" + histogramPnsr + "'<span></span></div>");

                // $("#pnsr-container-mamdani").html("<div class='block flex-col items-center h-full'><span class='text-small text-gray-500'>PNSR Fuzzy Mamdani Enhancement</span>'" + mamdaniPnsr + "'<span></span></div>");

                // $("#pnsr-container-sugeno").html("<div class='block flex-col items-center h-full'><span class='text-small text-gray-500'>PNSR Fuzzy Sugeno Enhancement</span>'" + sugenoPnsr + "'<span></span></div>");

                // $("#pnsr-container-tsukamoto").html("<div class='block flex-col items-center h-full'><span class='text-small text-gray-500'>PNSR Fuzzy Tsukamoto Enhancement</span>'" + tsukamotoPnsr + "'<span></span></div>");
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });

    });

    document.getElementById("btnPnsr").onclick = (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Perform AJAX request to the server
        $.ajax({
            url: "/calculate_pnsr",
            type: "POST",
            data: new FormData(document.getElementById("form-image-upload")),
            processData: false,
            contentType: false,
            success: function (response) {
                // Successful AJAX response
                const histogramPnsr = response.psnr_histogram
                // const mamdaniPnsr = response.mamdani_uri
                // const sugenoPnsr = response.sugeno_uri
                // const tsukamotoPnsr = response.tsukamoto_uri

                console.log(histogramPnsr);

                $('#calculate-pnsr').removeClass("hidden")
                $('#pnsr-container-histogram').text(histogramPnsr)
                // $('#pnsr-container-mamdani').text(mamdaniPnsr)
                // $('#pnsr-container-sugeno').text(sugenoPnsr)
                // $('#pnsr-container-tsukamoto').text(tsukamotoPnsr)

            },
            error: function (xhr, status, error) {
                // AJAX request error handling
                console.log(error);
            },
        });

    };

    // $('#enhancement').click(function () {
    //     alert('a');
    // });

    // // print all selected files
    // document.getElementById("submit").onclick = () => {
    //     alert(`Submitted Files:\n${JSON.stringify(FILES)}`);
    //     console.log(FILES);
    // };

    // clear entire selection
    // document.getElementById("cancel").onclick = () => {
    //     while (gallery.children.length > 0) {
    //         gallery.lastChild.remove();
    //     }
    //     FILES = {};
    //     empty.classList.remove("hidden");
    //     gallery.append(empty);

    //     $('#image-identify').addClass("hidden");
    // };

    document.getElementById("cancel").onclick = (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Clear the file input value
        document.getElementById("hidden-input").value = null;

        // Hide the pneumonia percentage element
        $('#image-identify').addClass("hidden");

        // Remove uploaded images from the gallery
        while (gallery.children.length > 0) {
            gallery.lastChild.remove();
        }
        FILES = {};
        empty.classList.remove("hidden");
        gallery.append(empty);

        $("#image-container").empty();
        $("#image-container-sugeno").empty();
        $("#image-container-tsukamoto").empty();
        // $('#enhancement').addClass("hidden")
        // $('#submit').removeClass('hidden')
        // $('#submit').addClass("visible")
    };

    const fileInput = document.getElementById('hidden-input');
    const submitButton = document.getElementById('submit');
    fileInput.addEventListener('change', function () {
        const file = this.files[0];
        const fileName = file.name;
        const fileExt = fileName.split('.').pop();

        // alert(fileExt)
        // Gunakan fileExt sesuai kebutuhan Anda
        // console.log(fileExt);

        // if (fileExt === 'dcm') {
        //     submitButton.disabled = false;
        // } else {
        //     submitButton.disabled = true;
        //     console.log('File extension is not .dcm');
        // }

    });


});