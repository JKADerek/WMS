// barcode_scanner.js

document.addEventListener('DOMContentLoaded', function() {
    if (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
        // QuaggaJS configuration
        var quaggaConfig = {
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#barcode-scanner') // Pass the ID of the video element
            },
            decoder: {
                readers: ["code_128_reader", "ean_reader", "ean_8_reader", "code_39_reader", "code_39_vin_reader", "codabar_reader", "upc_reader", "upc_e_reader", "i2of5_reader"] // Specify barcode formats to decode
            },
            locate: true // Enables barcode location within the image
        };

        // Initialize QuaggaJS
        Quagga.init(quaggaConfig, function(err) {
            if (err) {
                console.log(err);
                return;
            }
            console.log("QuaggaJS initialization successful.");
            Quagga.start();
        });

        // Handle detected barcodes
        Quagga.onDetected(function(data) {
            var barcode = data.codeResult.code;
            console.log("Barcode detected:", barcode);

            // You can make an AJAX call here to send the barcode to your server for processing
            // Example:
            // fetch('/process_barcode', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify({ barcode: barcode }),
            // })
            // .then(response => response.json())
            // .then(data => {
            //     console.log('Success:', data);
            // })
            // .catch((error) => {
            //     console.error('Error:', error);
            // });

            // Optionally, stop QuaggaJS after a successful scan
            // Quagga.stop();
        });
    } else {
        console.log("getUserMedia is not supported by this browser.");
    }
});
