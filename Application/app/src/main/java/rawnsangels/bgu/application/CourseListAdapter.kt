package rawnsangels.bgu.application

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import kotlinx.android.synthetic.main.course_list_item.view.*

class CourseListAdapter(val context: Context, data: List<Course>) : BaseAdapter() {

    internal var data: List<Course> = data
        set(value) {
            field = value
            notifyDataSetChanged()
        }

    override fun getCount() = data.size

    override fun getItem(i: Int) = data[i]

    override fun getItemId(i: Int) = i.toLong()

    override fun getView(i: Int, view: View?, viewGroup: ViewGroup): View {
        val listItemView = view ?:
        LayoutInflater.from(context).inflate(R.layout.course_list_item, viewGroup, false)

        val course = getItem(i)
        listItemView.courseTitle.text = course.name
        listItemView.departmentNum.text = course.departmentId.toString()
        listItemView.courseNum.text = course.courseId.toString()

        return listItemView
    }
}
