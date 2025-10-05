<template>
  <q-page class="q-pa-md">
    <div class="page-header q-mb-lg">
      <div>
        <h1 class="text-h5 text-weight-bold q-mb-xs">Employee Management System</h1>
        <p class="text-body2 text-grey-7">Manage your team members and their information</p>
      </div>
      <q-btn 
        unelevated
        color="primary" 
        icon="add"
        label="Add Employee"
        @click="openAddDialog"
        class="q-px-lg border-radius-20px"
        style="border-radius: 10px"
      />
    </div>

    <q-card flat bordered class="q-mb-md">
      <q-card-section class="q-py-md">
        <q-input 
          v-model="searchQuery" 
          outlined
          dense
          placeholder="Search by name, email, phone, position, or address..."
          debounce="300"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
          <template v-slot:append v-if="searchQuery">
            <q-icon name="close" class="cursor-pointer" @click="searchQuery = ''" />
          </template>
        </q-input>
      </q-card-section>
    </q-card>

    <q-card flat bordered class="employee-table-card">
      <q-table
        :rows="filteredEmployees"
        :columns="columns"
        :loading="loading"
        :pagination="pagination"
        @request="onTableRequest"
        row-key="id"
        flat
        class="employees-table"
      >
        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <q-avatar size="22px" color="primary" text-color="white" class="q-mr-sm">
                {{ getInitials(props.row.name) }}
              </q-avatar>
              <span class="text-weight-medium">{{ props.row.name }}</span>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-email="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <q-icon name="mail_outline" size="18px" class="q-mr-xs text-grey-6" />
              <span>{{ props.row.email }}</span>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-phone="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <q-icon name="phone" size="18px" class="q-mr-xs text-grey-6" />
              <span>{{ props.row.phone || 'N/A' }}</span>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-position="props">
          <q-td :props="props">
            <q-badge 
              color="blue-grey-2" 
              text-color="blue-grey-8"
              :label="props.row.position"
              class="q-px-md q-py-xs"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-address="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <q-icon name="location_on" size="18px" class="q-mr-xs text-grey-6" />
              <span>{{ props.row.address || 'N/A' }}</span>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <div class="row no-wrap q-gutter-xs">
              <q-btn 
                flat dense round icon="edit" color="primary" size="sm"
                @click="openEditDialog(props.row)"
              >
                <q-tooltip>Edit</q-tooltip>
              </q-btn>
              <q-btn 
                flat dense round icon="delete" color="negative" size="sm"
                @click="confirmDelete(props.row)"
              >
                <q-tooltip>Delete</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>

        <template v-slot:loading>
          <q-inner-loading showing color="primary" />
        </template>

        <template v-slot:no-data>
          <div class="full-width column items-center q-py-xl">
            <q-icon name="group_off" size="64px" color="grey-5" class="q-mb-md" />
            <p class="text-h6 text-grey-7">No employees found</p>
            <p class="text-body2 text-grey-6">
              {{ searchQuery ? 'Try adjusting your search criteria' : 'Get started by adding your first employee' }}
            </p>
          </div>
        </template>
      </q-table>
    </q-card>

    <q-dialog v-model="dialogOpen" persistent>
      <q-card style="min-width: 500px; max-width: 90vw; border-radius: 10px;">
        <q-card-section class="row items-center q-pb-sm q-pt-md">
          <div class="text-h6 text-primary">
            {{ isEditMode ? 'Edit Employee' : 'Add New Employee' }}
          </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup class="text-grey-7" />
        </q-card-section>

        <q-separator />

        <q-form @submit="handleSaveEmployee" class="q-pa-lg">
          <div class="q-gutter-md">
            <q-input 
              v-model="form.name" 
              label="Full Name" 
              outlined 
              dense 
              :rules="[val => !!val || 'Name is required']"
            >
              <template v-slot:prepend>
                <q-icon name="person" />
              </template>
            </q-input>

            <q-input 
              v-model="form.email" 
              label="Email Address" 
              type="email" 
              outlined 
              dense
              :rules="[
                val => !!val || 'Email is required',
                val => /.+@.+\..+/.test(val) || 'Invalid email format'
              ]"
            >
              <template v-slot:prepend>
                <q-icon name="mail" />
              </template>
            </q-input>

            <q-input 
              v-model="form.phone" 
              label="Phone Number" 
              outlined 
              dense
              :rules="[val => !!val || 'Phone number is required']"
            >
              <template v-slot:prepend>
                <q-icon name="phone" />
              </template>
            </q-input>

            <q-input 
              v-model="form.position" 
              label="Position" 
              outlined 
              dense
              :rules="[val => !!val || 'Position is required']"
            >
              <template v-slot:prepend>
                <q-icon name="work" />
              </template>
            </q-input>

            <q-input 
              v-model="form.address" 
              label="Address" 
              outlined 
              dense
              :rules="[val => !!val || 'Address is required']"
            >
              <template v-slot:prepend>
                <q-icon name="location_on" />
              </template>
            </q-input>
          </div>

          <div class="row justify-end q-gutter-sm q-mt-xl">
            <q-btn 
              flat 
              label="Cancel" 
              color="grey-7" 
              v-close-popup 
              class="q-px-md"
            />
            <q-btn 
              unelevated 
              type="submit" 
              :label="isEditMode ? 'Update' : 'Create'" 
              color="primary"
              :loading="saving" 
              class="q-px-md"
            />
          </div>
        </q-form>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useQuasar } from 'quasar';
import type { QTableColumn, QTableProps } from 'quasar';
import { 
  fetchEmployees, 
  createEmployee, 
  updateEmployee, 
  deleteEmployee 
} from 'src/services/EmployeeService';

const $q = useQuasar();

interface Employee {
  id: number | null;
  name: string;
  email: string;
  phone: string;
  position: string;
  address: string;
}

interface ApiErrorResponse {
  response?: {
    data?: {
      error?: string;
    };
  };
}

function isApiError(error: unknown): error is ApiErrorResponse {
  return (
    typeof error === 'object' &&
    error !== null &&
    'response' in error
  );
}

const employees = ref<Employee[]>([]);
const loading = ref(false);
const saving = ref(false);
const dialogOpen = ref(false);
const isEditMode = ref(false);
const searchQuery = ref('');

const form = ref<Employee>({
  id: null,
  name: '',
  email: '',
  phone: '',
  position: '',
  address: '',
});

const columns: QTableColumn[] = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' as const, sortable: true, style: 'width: 80px' },
  { name: 'name', label: 'Name', field: 'name', align: 'left' as const, sortable: true },
  { name: 'email', label: 'Email', field: 'email', align: 'left' as const, sortable: true },
  { name: 'phone', label: 'Phone', field: 'phone', align: 'left' as const, sortable: true },
  { name: 'position', label: 'Position', field: 'position', align: 'left' as const, sortable: true },
  { name: 'address', label: 'Address (Place)', field: 'address', align: 'left' as const, sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'left' as const, style: 'width: 120px' },
];

const pagination = ref({
  sortBy: 'id',
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
});

const filteredEmployees = computed(() => {
  if (!searchQuery.value) return employees.value;
  const query = searchQuery.value.toLowerCase();
  return employees.value.filter(emp => 
    emp.name?.toLowerCase().includes(query) ||
    emp.email?.toLowerCase().includes(query) ||
    emp.phone?.toLowerCase().includes(query) ||
    emp.position?.toLowerCase().includes(query) ||
    emp.address?.toLowerCase().includes(query)
  );
});

function getInitials(name: string): string {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

async function loadEmployees(): Promise<void> {
  loading.value = true;
  try {
    const data = await fetchEmployees();
    employees.value = data;
    pagination.value.rowsNumber = data.length;
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to load employees',
      caption: error instanceof Error ? error.message : 'Unknown error',
      position: 'top'
    });
  } finally {
    loading.value = false;
  }
}

function openAddDialog(): void {
  isEditMode.value = false;
  form.value = { id: null, name: '', email: '', phone: '', position: '', address: '' };
  dialogOpen.value = true;
}

function openEditDialog(employee: Employee): void {
  isEditMode.value = true;
  form.value = { ...employee };
  dialogOpen.value = true;
}

async function saveEmployee(): Promise<void> {
  saving.value = true;
  try {
    const data = {
      name: form.value.name,
      email: form.value.email,
      phone: form.value.phone,
      position: form.value.position,
      address: form.value.address,
    };
    if (isEditMode.value) {
      await updateEmployee(form.value.id, data);
      $q.notify({ type: 'positive', message: 'Employee updated successfully', position: 'top' });
    } else {
      await createEmployee(data);
      $q.notify({ type: 'positive', message: 'Employee created successfully', position: 'top' });
    }
    await loadEmployees();
    dialogOpen.value = false;
  } catch (error: unknown) {
    const errorMessage = isApiError(error) 
      ? error.response?.data?.error || 'Operation failed'
      : 'Operation failed';
    $q.notify({ type: 'negative', message: errorMessage, position: 'top' });
  } finally {
    saving.value = false;
  }
}

function handleSaveEmployee(): void {
  saveEmployee().catch(err => console.error(err));
}

function confirmDelete(employee: Employee): void {
  $q.dialog({
    title: 'Confirm Deletion',
    message: `Are you sure you want to delete ${employee.name}?`,
    cancel: true,
    persistent: true
  }).onOk(() => {
    handleDelete(employee);
  });
}

function handleDelete(employee: Employee): void {
  executeDelete(employee).catch(err => console.error(err));
}

async function executeDelete(employee: Employee): Promise<void> {
  try {
    await deleteEmployee(employee.id);
    $q.notify({
      type: 'warning',
      message: `${employee.name} has been deleted`,
      position: 'top'
    });
    await loadEmployees();
  } catch (error: unknown) {
    const errorMessage = isApiError(error)
      ? error.response?.data?.error || 'Deletion failed'
      : 'Deletion failed';
    $q.notify({ type: 'negative', message: errorMessage, position: 'top' });
  }
}

function onTableRequest(props: Parameters<NonNullable<QTableProps['onRequest']>>[0]): void {
  const { sortBy, descending, page, rowsPerPage, rowsNumber } = props.pagination;
  pagination.value = { sortBy, descending, page, rowsPerPage, rowsNumber: rowsNumber ?? 0 };
}

onMounted(() => {
  loadEmployees().catch(err => console.error(err));
});
</script>

<style lang="scss" scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.employees-table {
  :deep(.q-table__top) {
    padding: 16px;
  }

  :deep(.q-table thead tr) {
    background-color: #f5f5f5;
  }

  :deep(.q-table tbody td) {
    font-size: 14px;
  }

  :deep(.q-table__card) {
    box-shadow: none;
  }

  .employee-table-card {
    border-radius: 10px;
    overflow: hidden;
  }
}

</style>
