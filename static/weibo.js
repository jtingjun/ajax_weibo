// Weibo API
// 获取所有 Weibo
var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weiboId, callback) {
    var path = `/api/weibo/delete?id=${weiboId}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(commentId, callback) {
    var path = `/api/comment/delete?id=${commentId}`
    ajax('GET', path, '', callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = `/api/comment/update`
    ajax('POST', path, form, callback)
}

var weiboTemplate = function(weibo) {
    var t = `
        <div class="weibo-cell" data-id="${weibo.id}">
            <span class="weibo-content">${weibo.content}</span> <span> from ${weibo.username}</span>
            <button class="weibo-delete">删除</button>
            <button class="weibo-edit">编辑</button>
            <br>
            <input class="weibo-comment-input">
            <button class="weibo-add-comment">添加评论</button>
            <br>
        </div>
    `
    return t
}

var weiboUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${content}">
            <button class="weibo-update">更新</button>
        </div>
    `
    return t
}

var commentTemplate = function(comment) {
    var t = `
        <div class="weibo-comment" data-id="${comment.id}">
            ${comment.username} : <span class="comment-content">${comment.content}</span>
            <button class='comment-delete'>删除评论</button>
            <button class='comment-edit'>编辑评论</button>
        </div>
    `
    return t
}

var commentUpdateTemplate = function(content) {
    var t = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${content}">
            <button class="comment-update">更新</button>
        </div>
    `
    return t
}

var insertWeibo = function(weibo, commentCells) {
    var weiboCell = weiboTemplate(weibo)
    var weiboWithComment = '<div>' + weiboCell + commentCells +'</div> <br>'
    // 插入 weibo-list
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboWithComment)
}

var insertUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

var insertComment = function(weiboCell, comment) {
    var comment = commentTemplate(comment)
    weiboCell.insertAdjacentHTML('afterend', comment)
}

var insertCommentUpdateForm = function(content, commentCell) {
    var updateForm = commentUpdateTemplate(content)
    commentCell.insertAdjacentHTML('beforeend', updateForm)
}

var loadWeibos = function() {
    apiWeiboAll(function(weibos) {
        log('load all weibos', weibos)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            var comments = weibo.comments
            //
            var commentCells = ''
            for (var j = 0; j < weibo.comments.length; j++) {
                var c = commentTemplate(comments[j])
                commentCells += c
            }
            insertWeibo(weibo, commentCells)
        }
    })
    // second call
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo, '')
        })
    })
}

var bindEventWeiboDelete = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('weibo-delete')) {
        log('点到了删除按钮')
        weiboId = self.parentElement.dataset['id']
        apiWeiboDelete(weiboId, function(r) {
            log('apiWeiboDelete', r.message)
            // 删除 self 的父节点
            self.parentElement.remove()
            alert(r.message)
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('weibo-edit')) {
        log('点到了编辑按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        var weiboSpan = e('.weibo-content', weiboCell)
        var content = weiboSpan.innerText
        // 插入编辑输入框
        insertUpdateForm(content, weiboCell)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('weibo-update')) {
        log('点到了更新按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        log('update weibo id', weiboId)
        input = e('.weibo-update-input', weiboCell)
        content = input.value
        var form = {
            id: weiboId,
            content: content,
        }

        apiWeiboUpdate(form, function(weibo) {
            // 收到返回的数据, 插入到页面中
            log('apiweiboUpdate', weibo)
            if (weibo.message === '您没有此操作的权限！') {
                alert(weibo.message)
                var updateForm = e('.weibo-update-form', weiboCell)
                updateForm.remove()
            } else {
                var weiboSpan = e('.weibo-content', weiboCell)
                weiboSpan.innerText = weibo.content

                var updateForm = e('.weibo-update-form', weiboCell)
                updateForm.remove()
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentAdd = function () {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('weibo-add-comment')) {
        log('点到了添加按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        input = e('.weibo-comment-input', weiboCell)
        content = input.value
        var form = {
            weibo_id: weiboId,
            content: content,
        }
        apiCommentAdd(form, function(comment) {
            // 收到返回的数据, 插入到页面中
            log('comment', comment)
            insertComment(weiboCell, comment)
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentDelete = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    log('self', self.classList)
    if (self.classList.contains('comment-delete')) {
        log('点到了删除按钮')
        commentId = self.parentElement.dataset['id']

        apiCommentDelete(commentId, function(r) {
            // 删除 self 的父节点
            if (r.message === '您没有此操作的权限！') {
                alert(r.message)
            } else {
                self.parentElement.remove()
                alert(r.message)
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-edit')) {
        log('点到了编辑按钮')
        commentCell = self.closest('.weibo-comment')
        commentId = self.parentElement.dataset['id']
        var commentSpan = e('.comment-content', commentCell)
        var content = commentSpan.innerText
        // 插入编辑输入框
        insertCommentUpdateForm(content, commentCell)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-update')) {
        log('点到了更新按钮')
        commentCell = self.closest('.weibo-comment')
        commentId = commentCell.dataset['id']
        input = e('.comment-update-input', commentCell)
        var content = input.value
        var form = {
            id: commentId,
            content: content,
        }

        apiCommentUpdate(form, function(comment) {
            // 收到返回的数据, 插入到页面中
            if (comment.message === '您没有此操作的权限！') {
                alert(comment.message)
                var updateForm = e('.comment-update-form', commentCell)
                updateForm.remove()
            } else {
                var commentSpan = e('.comment-content', commentCell)
                commentSpan.innerText = comment.content

                var updateForm = e('.comment-update-form', commentCell)
                updateForm.remove()
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}


var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
