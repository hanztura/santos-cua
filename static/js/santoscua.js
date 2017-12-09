$('.action-delete').click(function(e){
    if (!confirm('Are you sure to delete this record?')) {
        e.preventDefault()
        return
    } else {
    }
})
$('.action-logout').click(function(e){
    if (!confirm('Continue logout?')) {
        e.preventDefault()
        return
    } else {
    }
})
$('.action-download').click(function(e){
    if (!confirm('Continue download?')) {
        e.preventDefault()
        return
    }
})

$('.action-save').click(function(e){
    if (!confirm('Kindly make sure to review entries. Continue saving?')) {
        e.preventDefault()
        return
    } else {
    }
})

$('.action-detail').click(function(e){
    alias = $(this).data('action-alias')
    if (!confirm('View ' + alias + '\s detail?')) {
        e.preventDefault()
        return
    } else {
    }
})

// modal
$('#modal-confirm-action').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var title = button.data('title') // Extract info from data-* attributes
  var url = button.data('url') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text(title)
  modal.find('.modal-url').attr('href', url)
})
$('#modal-confirm-submit').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var title = button.data('title') // Extract info from data-* attributes
  var url = button.data('url') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text(title)
  modal.find('.modal-url').attr('action', url)
})