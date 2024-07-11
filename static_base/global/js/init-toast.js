const toastlist = document.getElementsByClassName('toast')

Array.from(toastlist).forEach(toast => {
    const boot = bootstrap.Toast.getOrCreateInstance(toast)
    boot.show()
})
