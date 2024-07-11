window.addEventListener('DOMContentLoaded', () => {
    let delete_forms = document.getElementsByClassName('delete-submit')

    Array.from(delete_forms).map((form) => {
        form.addEventListener('submit', (e) => {
            e.preventDefault()
            if (window.confirm('Do you want to delete? this operation is irreversible')) {
                e.stopPropagation()
                form.submit()
            }
        })
    })

})
