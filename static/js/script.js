// ********rental_cars.html ************

const modal = document.getElementById("rentalModal");
if (modal){
    const openModalBtn = document.getElementById("openModalBtn");
    const closeModalBtn = document.getElementById("closeModalBtn");
    const rentalForm = document.getElementById("rentalForm");
    const calculateBtn = document.getElementById("calculate");
    const totalAmountP = document.getElementById('totalAmount')

    // Show the modal when button is clicked
    openModalBtn.onclick = function () {
        modal.style.display = "block";
    };

    // Close the modal when the close button is clicked
    closeModalBtn.onclick = function () {
        modal.style.display = "none";
    };

    // Close modal if user clicks outside of modal content
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };


    calculateBtn.onclick = () => {
        const carId = document.getElementById('carId');

        const price_Per_Week = Number(carId.dataset.price_per_week);
        const price_Per_Day = Number(carId.dataset.price_per_day);

        const startDate = document.getElementById('rentalStartDate').value;
        const endDate = document.getElementById('rentalEndDate').value;
        let amount = 0

        if (startDate && endDate && endDate > startDate) {
            const start = new Date(startDate);
            const end = new Date(endDate);

            const total_days = (end - start) / (1000 * 60 * 60 * 24);


            if (total_days => 7) {
                const week = Math.floor(total_days / 7);
                const remaing_dates = total_days % 7
                amount = ((week * price_Per_Week) + (remaing_dates * (price_Per_Week / 7)))
                totalAmountP.innerText = amount.toFixed(2)
                calculated_amound.value = amount.toFixed(2)
            }
            else {
                amount = (total_days * price_Per_Day)
                totalAmountP.innerText = amount.toFixed(2)
                calculated_amound.value = amount.toFixed(2)

            }

        }
        else {
            alert('End date must be after start date.');
        }

    };
    // Form submission to calculate total
    rentalForm.onsubmit = function (event) {
        const calculated_amound = document.getElementById('calculated_amound');
        const calculated_amound_value = Number(calculated_amound.value);
        console.log(calculated_amound_value);

        if (!calculated_amound_value || parseFloat(calculated_amound_value) <= 0) {
            event.preventDefault();
            alert("plese calculate total amount before submiting")
        }
    };
}

const messagemodal = document.getElementById('messageModal')
if(messagemodal){
    const closeBtn = document.getElementById('closeMessageModalBtn')


    document.addEventListener('DOMContentLoaded',()=>{
        messagemodal.style.display = 'block'
    })

    closeBtn.onclick=()=>{
        messagemodal.style.display = "none"
    }
    window.onclick = function (event) {
        if (event.target == messagemodal ) {
            messagemodal.style.display = "none";
        }
    };

}

const feedbackmodal = document.getElementById('FeedbackModal')
if (feedbackmodal){
    document.addEventListener('DOMContentLoaded',()=>{
        document.body.addEventListener('click',(event)=>{
            if (event.target && event.target.id === 'feedbackbtn' ){
                feedbackmodal.style.display = 'block'
            }
            if (event.target && event.target.id === 'closeFeedbackModalBtn') {
                feedbackmodal.style.display = 'none'
            }

            window.onclick = function (event) {
                    if (event.target == feedbackmodal) {
                        feedbackmodal.style.display = "none";
                    }
                };

            
        })
    })
}

issue=document.getElementById('issue')
if(issue){
    const completed = document.getElementById('completed')
    const in_progress = document.getElementById('in_progress')
    const canceled = document.getElementById('cancel')
    const accept = document.getElementById('accept')
    if (completed){
        completed.style.color = 'green'
    }
    if (canceled){
        canceled.style.color = 'red'
    }
    if(accept){
        accept.style.color = 'blue'   
    }
    if(in_progress){
        in_progress.style.color = 'orange'

    }
}


