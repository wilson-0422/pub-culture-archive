document.addEventListener('DOMContentLoaded', function () {
  var flashMessages = document.querySelector('.flash-messages')
  if (flashMessages) {
    setTimeout(function () {
      flashMessages.style.transition = 'opacity 0.5s'
      flashMessages.style.opacity = '0'
      setTimeout(function () {
        flashMessages.remove()
      }, 500)
    }, 4000)
  }

  var searchInput = document.querySelector('.search-input')
  if (searchInput) {
    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.target.closest('form').submit()
      }
    })
  }

  var deleteForms = document.querySelectorAll('form[onsubmit*="confirm"]')
  deleteForms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!confirm('确定要执行此操作吗？')) {
        e.preventDefault()
      }
    })
  })
})
