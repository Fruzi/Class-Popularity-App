package rawnsangels.bgu.application

import android.os.Bundle
import android.support.v4.app.ListFragment
import android.support.v7.app.AlertDialog
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.ListView
import android.widget.Toast
import io.realm.Realm
import io.realm.RealmChangeListener
import io.realm.kotlin.where
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.new_course_dialog.view.*

class CourseListFragment : ListFragment() {

    private lateinit var realm: Realm
    private lateinit var realmChangeListener: RealmChangeListener<Realm>
    private lateinit var mListAdapter: CourseListAdapter

    private val activity: MainActivity
        get() = getActivity() as MainActivity

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        realm = Realm.getDefaultInstance()
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? =
            inflater.inflate(R.layout.fragment_course_list, container, false)

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        mListAdapter = CourseListAdapter(activity, realm.where<Course>().findAll())
        listAdapter = mListAdapter
        realmChangeListener = RealmChangeListener { updateList() }
        realm.addChangeListener(realmChangeListener)

        activity.fabAddCourse.setOnClickListener {
            // open new course dialog
            if (activity.depsCourses.isEmpty()) return@setOnClickListener
            val dialogView = View.inflate(activity, R.layout.new_course_dialog, null)
            dialogView.departmentSpinner.adapter = ArrayAdapter<String>(activity,
                    android.R.layout.simple_spinner_dropdown_item,
                    activity.depsCourses.keys.toList())
            dialogView.CourseSpinner.adapter = ArrayAdapter<String>(activity,
                    android.R.layout.simple_spinner_dropdown_item,
                    activity.depsCourses[dialogView.departmentSpinner.selectedItem]
                    !!.map { "${it.courseNumber} ${it.name}" })
            dialogView.departmentSpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                override fun onNothingSelected(parent: AdapterView<*>?) {

                }

                override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                    dialogView.CourseSpinner.adapter = ArrayAdapter<String>(activity,
                            android.R.layout.simple_spinner_dropdown_item,
                            activity.depsCourses[dialogView.departmentSpinner.selectedItem]
                            !!.map { "${it.courseNumber} ${it.name}" })
                }
            }
            val dialog = AlertDialog.Builder(activity)
                    .setTitle(R.string.new_course)
                    .setView(dialogView)
                    .setPositiveButton(R.string.add_course) { _, _ ->
                        // addCourse()
                        val depName = dialogView.departmentSpinner.selectedItem.toString()
                        val courseNum = dialogView.CourseSpinner.selectedItem.toString()
                            .split(" ")[0]
                        val courseObj = activity.depsCourses[depName]?.find {
                            it.courseNumber == courseNum
                        }!!
                        addCourse(courseObj)
                    }
                    .setNegativeButton(android.R.string.cancel, null)
                    .create()
            dialog.show()
        }
    }

    override fun onListItemClick(l: ListView?, v: View?, position: Int, id: Long) {
        Log.v("onListItemClick", v.toString())
    }

    override fun onDestroy() {
        super.onDestroy()
        realm.removeChangeListener(realmChangeListener)
        realm.close()
    }

    private fun addCourse(course: Course) {
        if (realm.where<Course>().equalTo("courseId", course.courseId).findFirst() == null) {
            realm.executeTransaction {
                realm.insert(course)
            }
            Toast.makeText(activity,
                    "Course added: ${course.departmentId} ${course.courseId} ${course.name}",
                    Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(activity, "Course already exists", Toast.LENGTH_SHORT).show()
        }
    }

    fun updateList() {
        mListAdapter.data = realm.where<Course>().findAll()
    }

    companion object {

        fun newInstance(): CourseListFragment {
            return CourseListFragment()
        }
    }
}
