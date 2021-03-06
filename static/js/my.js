var jobs, job_link;

function setLocations() {
	$.ajax({
		url:"/getLocations",
        dataType: "json", 
        success: function (data) {
        	setDropdownList('Location', data)
        }
	});
}

function setCategories() {
	var categories;
	$.ajax({
		url:"/getCategories",
        dataType: "json", 
        success: function (data) { 
        	setDropdownList('Category', data)
        }
	});
}

function setDropdownList(type, data) {
	var dropdownList = $('#dropdownList'+type), li, a, showee,
		dropdownButton = $('#dropdownButton'+type), 
		current = dropdownButton.data('value');
    data.push(' 全部');
	data.sort();
	dropdownList.html('');
	$.each(data, function(i, item) {
		a = $('<a></a>');
		a.attr('href', 'javascript:void(0);');
		a.attr('onclick', 'select("'+type+'","'+(item==' 全部'?'':item)+'")');
		a.attr('title', item);
		if(item.length > 15) {
			item = item.slice(0, 14) + '..';
		}
		a.html(item);
		li = $('<li></li>');
		li.append(a);
		dropdownList.append(li);
	});
}

function select(type, item) {
	var dropdownButton = $('#dropdownButton'+type),
		showee = item.length>20 ? item.slice(0,19)+'..' : item;
	if(showee == dropdownButton.html() || 
		(showee == ' 全部' && dropdownButton.html().indexOf('caret')>-1)) {
		return;
	}
	if(showee == '') {
		switch(type) {
			case 'Location':
				showee = '工作地址<span class="caret">';
				break;
			case 'Category':
				showee = '岗位类别<span class="caret">';
				break;
		}
		dropdownButton.data('value', '');
	} else {
		dropdownButton.data('value', item);
	}
	dropdownButton.html(showee);
	dropdownButton.attr('title', item);
	search();
//	get_other_menu_items(type, item);
}

function reload_other_menus(except, other_menus_items) {
	var menu_list = ['Location', 'Category'];
	
	$.each(menu_list, function(i, menu_name) {
		if(except != menu_name) {
			setDropdownList(menu_name, other_menus_items[menu_name.toLowerCase()]);
		}
	});
}

function search() {
	var location = getOption('Location'),
		category = getOption('Category'),
		keyword = $('#search_input').val(),
		formData = new FormData($('#csrfForm')[0]),
		that = this;
	formData.append("location", location);
	formData.append("category", category); 
	formData.append("keyword", keyword); 
	
	$('.table-responsive').remove();
	$('.pag_div').remove();
	$('#hint').remove();
	$('.query_hint').show();
	
	$.ajax({
 		type: 'POST',
		url:"/getJobs/",
  		data: formData,
        dataType: "json", 
        processData: false,
        contentType: false,
        success: function (data) {
        	that.jobs = JSON.parse(data);
        	turn_to_page(1);
        	$('.query_hint').hide();
        } 
	});
}

function turn_to_page(page) {
	var tbody, tr, td, a, span, job, i, table_wrapper,
		base = (page-1)*10,
		main = $('#container');
	
	$('.table-responsive').remove();
	$('.pag_div').remove();
	$('#hint').remove();
	
	table_wrapper = $('<div></div>');
	table_wrapper.addClass('table-responsive');
	
	tbody = $('<table></table>');
	tbody.addClass('table table-striped job-table');
	
	if (this.jobs.length == 0) {
		show_blank_page();
		return;
	}
		tr = $('<tr></tr>');
		
		td = $('<th></th>');
		td.html('职位名称');
		tr.append(td);
		
		td = $('<th></th>');
		td.html('地点');
		tr.append(td);
		
		td = $('<th></th>');
		td.html('类别');
		tr.append(td);
		
		td = $('<th></th>');
		td.html('职位简介');
		tr.append(td);
		
		tbody.append(tr);
	for(i=0 ; i<10 ; i++) {
		if(base+i >= this.jobs.length) {
			break;
		}
		job = this.jobs[base+i].fields;
		tr = $('<tr></tr>');
		td = $('<td></td>');
		
		a = $('<a></a>');
		a.attr('href', job.link);
		a.attr('target', '_blank');
		a.html(job.name);
		a.on("click", function(event){
			open_job($(this), event);
		});
		td.append(a);
		
		if(job.bonus) {
			span = $('<span></span>');
			span.addClass('glyphicon glyphicon-usd');
			span.attr('title', '应聘该职位成功可赢取奖金');
			td.append(span);
		}
		
		tr.append(td);
		
		td = $('<td></td>');
		td.html(job.location);
		tr.append(td);
		
		td = $('<td></td>');
		td.html(job.category);
		tr.append(td);
		
		td = $('<td></td>');
		td.html(job.description);
		tr.append(td);
		
		tbody.append(tr);
	}
	
	table_wrapper.append(tbody);
	main.append(table_wrapper);
	set_pagination(page);
	window.scrollTo(0,0);
}

function open_job(link, event) {
	if(!$.cookie('no_show_modal')) {
		event.preventDefault();
		$('#myModal').modal('show');
		job_link = link.attr('href');
	} else {
		$('a:focus').blur();
	}
}

function show_blank_page() {
	var hint;
	hint = $("<div><div>");
	hint.attr('id', 'hint');
	hint.attr('role', 'alert');
	hint.addClass('alert alert-info');
	hint.html('没有找到符合要求的职位，请尝试其他筛选条件');
	$("#container").append(hint);
}

function set_pagination(current) {
	var length = this.jobs.length,
	pages_num = parseInt((length-1)/10)+1,
	wrapper, nav, ul, li, a, i,
	start = 1, end = pages_num,
	left_arrow = false, right_arrow = false;

	wrapper = $('<div></div>');
	wrapper.addClass('pag_div');
	
	nav = $('<nav></nav>');
	
	ul = $('<ul></ul>');
	ul.addClass('pagination');
	
	if(current > 5) {
		start = current-4;
		left_arrow = true;
	}
	if(current+4 < pages_num) {
		end = current+4;
		right_arrow = true;
	}
	
	if(left_arrow) {
		li = $('<li></li>');
		a = $('<a></a>');
		a.attr('href', 'javascript:void(0);');
		a.html('&laquo;');
		a.on("click", function() {
			turn_to_page(current-1);
		});
		li.append(a);
		ul.append(li);
		
		li = $('<li></li>');
		a = $('<a></a>');
		a.attr('href', 'javascript:void(0);');
		a.html(1);
		a.on("click", function() {
			turn_to_page(1);
		});
		li.append(a);
		ul.append(li);
		
		li = $('<li></li>');
		a = $('<a></a>');
		a.html('..');
		li.append(a);
		ul.append(li);
		
		start++;
	}
	if(right_arrow) {
		end--;
	}
	for (i=start ; i<=end ; i++) {
		li = $('<li></li>');
		if(i == current) {
			li.addClass('active');
		}
		a = $('<a></a>');
		a.attr('href', 'javascript:void(0);');
		a.html(i);
		a.on("click", function(i){
			return function() {
				turn_to_page(i);
			}
		}(i));
		li.append(a);
		ul.append(li);
	}
	if(right_arrow) {
		li = $('<li></li>');
		a = $('<a></a>');
		a.html('..');
		li.append(a);
		ul.append(li);
		
		li = $('<li></li>');
		a = $('<a></a>');
		a.attr('href', 'javascript:void(0);');
		a.html(pages_num);
		a.on("click", function() {
			turn_to_page(pages_num);
		});
		li.append(a);
		ul.append(li);
		
		li = $('<li></li>');
		a = $('<a></a>');
		a.attr('href', 'javascript:void(0);');
		a.html('&raquo;');
		a.on("click", function() {
			turn_to_page(current+1);
		});
		li.append(a);
		ul.append(li);
	}
	
	nav.append(ul);
	wrapper.append(nav);
	$('#container').append(wrapper);
}

function getOption(id) {
	var dropdownButton = $('#dropdownButton'+id);
	return dropdownButton.data('value')
}

$().ready(function(){
	if($('#modal_close_button')) {
		$('#modal_close_button').on('click', function(){
			window.open(job_link);
			job_link = null;
			if($('#never_show').prop('checked')){
				$.cookie('no_show_modal', true, {path: '/'});
			}
		});
	}
	if(window.location.pathname != '/') {
		$("td a").on("click", function(event){
			open_job($(this), event);
		});
		return;
	}
	setLocations();
	setCategories();
	$('#search_button').on('click', function(event){
		event.preventDefault();
		search();
		$('#search_button').blur();
	});
	$('#clear_button').on('click', function(event){
		$('#search_input').val('');
		select('Category', '');
		select('Location', '');
		event.preventDefault();
		search();
		$('#clear_button').blur();
	});
	$('#billboard').children('button').on('click', function(event){
		$('#billboard').remove();
	});
	search();
})