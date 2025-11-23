
const deleteConfirm = document.getElementById('delete-confirm')
let deleteId = null
let deleteTitle = null
function showDeleteConfirm(postId, title) {
    deleteId = postId
    deleteTitle = title
    const target = document.getElementById('delete-confirm')
    document.getElementById('delete-title').textContent = 'Delete post: ' + deleteTitle
    target.style.display = 'flex'
    // 强制重排（避免动画不触发）
    void target.offsetWidth
    target.classList.add('show')

}
function hideDeleteConfirm() {
    deleteConfirm.style.display = 'none'
    deleteConfirm.classList.remove('show')
}

function deletePost() {
    if (!deleteId) {
        return
    }
    fetch('/delete/' + deleteId, {
        method: 'DELETE'
    }).then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok')
        }
        return response.json()
    }).then((json) => {
        if (json?.message === 'success') {
            document.getElementById('post-' + deleteId).remove()
            hideDeleteConfirm()
        }
    }).catch((error) => {
        alert('Error: ' + error)
    })
}