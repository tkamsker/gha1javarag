"""
UI Modernization Processor for Iteration 14
Generates modern UI architecture requirements and migration strategies from Weaviate UI analysis
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class UIModernizationProcessor:
    """Processes UI analysis results to generate comprehensive modernization and migration documentation"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.ui_modern_dir = self.output_dir / "requirements_modern" / "ui"
        self.ui_modern_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for organized modern requirements
        (self.ui_modern_dir / "migration_strategy").mkdir(exist_ok=True)
        (self.ui_modern_dir / "component_mapping").mkdir(exist_ok=True)
        (self.ui_modern_dir / "modern_architecture").mkdir(exist_ok=True)
        (self.ui_modern_dir / "progressive_web_app").mkdir(exist_ok=True)
        (self.ui_modern_dir / "design_system").mkdir(exist_ok=True)
    
    def generate_component_migration_mapping(self, ui_analysis: Dict[str, Any]) -> str:
        """Generate detailed component-to-modern-framework migration mapping"""
        ui_components = ui_analysis.get('ui_components', {})
        modernization_analysis = ui_analysis.get('modernization_analysis', {})
        timestamp = datetime.now().isoformat()
        
        content = f"""# GWT to Modern Framework Component Migration Mapping

**Generated**: {timestamp}
**Category**: Component_Migration_Mapping
**Mode**: enhanced_ui_analysis

## 1. MIGRATION MAPPING OVERVIEW

### 1.1 Component Migration Statistics

**Migration Scope:**
- **Total Components to Migrate**: {len(ui_components)}
- **High Priority Migrations**: {modernization_analysis.get('high_priority_count', 0)} components
- **Medium Priority Migrations**: {modernization_analysis.get('medium_priority_count', 0)} components  
- **Low Priority Migrations**: {modernization_analysis.get('low_priority_count', 0)} components
- **Average Component Complexity**: {modernization_analysis.get('average_complexity_score', 0):.1f}/100

### 1.2 Technology Stack Migration

**From GWT Architecture:**
- Google Web Toolkit (GWT) 2.x framework
- Java-to-JavaScript compilation
- UiBinder XML templates for UI definition
- GWT widgets and custom composites
- RPC-based server communication

**To Modern React Architecture:**
- React 18+ with TypeScript for type safety
- JSX templates with component composition
- Material-UI (MUI) v5 component library
- React Hooks for state and lifecycle management
- RESTful APIs with React Query for data fetching

## 2. COMPONENT TYPE MAPPING

### 2.1 Portlet Components Migration

**GWT Portlet → React Card Component**

**Components to Migrate**: {len([comp for comp in ui_components.values() if comp.component_type == 'portlet'])} portlets identified

**Migration Pattern:**
```typescript
// Before (GWT)
public class ProductAdministrationPortletView extends Composite {{
    @UiField ScrollPanel mainPanel;
    @UiField CellTree productTree;
    
    @UiHandler("productTree")
    void onSelectionChange(SelectionChangeEvent event) {{
        // Handle selection
    }}
}}

// After (React + TypeScript + MUI)
interface ProductAdministrationProps {{
    onProductSelect: (productId: string) => void;
}}

const ProductAdministrationCard: React.FC<ProductAdministrationProps> = (props) => {{
    const [selectedProduct, setSelectedProduct] = useState<string | null>(null);
    
    return (
        <Card sx={{{{ height: '100%' }}}}>
            <CardHeader title="Product Administration" />
            <CardContent>
                <TreeView onNodeSelect={{(productId) => {{
                    setSelectedProduct(productId);
                    props.onProductSelect(productId);
                }}}}>
                    // Tree content
                </TreeView>
            </CardContent>
        </Card>
    );
}};
```

**Key Migration Benefits:**
- TypeScript provides compile-time type safety
- Material-UI ensures consistent design system
- React hooks simplify state management
- Better accessibility with semantic HTML and ARIA
- Mobile-first responsive design out of the box

"""
        
        # Add specific portlet migration plans
        portlets = [comp for comp in ui_components.values() if comp.component_type == 'portlet']
        if portlets:
            content += "**Specific Portlet Migration Plans:**\n\n"
            
            for i, portlet in enumerate(portlets[:5], 1):
                mui_components = self._get_suggested_mui_components(portlet)
                migration_time = self._estimate_migration_time(portlet)
                
                content += f"""**{i}. {portlet.component_name}**
- **Complexity Score**: {portlet.ui_complexity_score}/100
- **Migration Complexity**: {portlet.migration_complexity}
- **Modern Component**: Material-UI Card with {mui_components}
- **State Management**: {'Redux slice' if portlet.ui_complexity_score > 60 else 'Local component state with useState'}
- **Testing Strategy**: Jest + React Testing Library with {len(portlet.event_handlers)} interaction tests
- **Migration Timeline**: {migration_time} development days

"""

        content += """### 2.2 Dialog Components Migration

**GWT DialogBox → MUI Dialog Components**

**Migration Approach:**
- Replace GWT DialogBox with Material-UI Dialog
- Implement proper focus management and accessibility
- Add responsive behavior for mobile devices
- Integrate with React Hook Form for form dialogs

**Modern Dialog Pattern:**
```typescript
interface EditUserDialogProps {{
    open: boolean;
    user?: User;
    onClose: () => void;
    onSave: (user: User) => Promise<void>;
}}

const EditUserDialog: React.FC<EditUserDialogProps> = ({{
    open, user, onClose, onSave
}}) => {{
    const {{ control, handleSubmit, formState: {{ isValid }} }} = useForm<User>();
    
    return (
        <Dialog 
            open={{open}} 
            onClose={{onClose}}
            maxWidth="md"
            fullWidth
            aria-labelledby="edit-user-title"
        >
            <DialogTitle id="edit-user-title">
                {{user ? 'Edit User' : 'Create User'}}
            </DialogTitle>
            <DialogContent>
                <UserForm control={{control}} />
            </DialogContent>
            <DialogActions>
                <Button onClick={{onClose}}>Cancel</Button>
                <Button 
                    variant="contained" 
                    onClick={{handleSubmit(onSave)}}
                    disabled={{!isValid}}
                >
                    Save
                </Button>
            </DialogActions>
        </Dialog>
    );
}};
```

"""

        # Add dialog migration details
        dialogs = [comp for comp in ui_components.values() if comp.component_type == 'dialog']
        if dialogs:
            content += f"**Dialog Migration Details**: {len(dialogs)} dialogs requiring modernization\n\n"
            
            for dialog in dialogs[:3]:
                content += f"- **{dialog.component_name}**: {dialog.migration_complexity} complexity\n"

        content += """
### 2.3 Widget and Component Library Migration

**GWT Widgets → Material-UI Components**

**Widget Mapping Table:**
| GWT Widget | Material-UI Component | Additional Features |
|------------|----------------------|-------------------|
| ScrollPanel | Box with overflow: 'auto' | Better scroll behavior |
| CellTree | TreeView from MUI Lab | Virtualization for performance |
| RadioButton | Radio with RadioGroup | Better accessibility |
| TextBox | TextField | Built-in validation |
| Button | Button | Multiple variants and sizes |
| ListBox | Select or Autocomplete | Better UX patterns |
| Grid | DataGrid from MUI X | Advanced features |
| MenuBar | Menu with MenuList | Keyboard navigation |
| TabPanel | Tabs with TabPanel | Smooth animations |
| DialogBox | Dialog | Focus management |

**Custom Widget Migration:**
For complex custom GWT widgets, the migration strategy involves:
1. **Analysis**: Break down widget functionality into core features
2. **Composition**: Combine Material-UI primitives to recreate functionality  
3. **Enhancement**: Add modern features (accessibility, responsive design)
4. **Testing**: Comprehensive testing including visual regression tests

## 3. NAVIGATION AND ROUTING MODERNIZATION

### 3.1 Navigation Flow Migration

**From GWT History Management to React Router:**
"""
        
        nav_flows = ui_analysis.get('navigation_flows', [])
        if nav_flows:
            avg_complexity = sum(f.flow_complexity for f in nav_flows) / len(nav_flows)
            complex_flows = [f for f in nav_flows if f.flow_complexity >= 3]
            
            content += f"""
**Current Navigation Flows**: {len(nav_flows)} workflows identified

**Migration Strategy:**
- Replace GWT History API with React Router v6
- Implement nested routing for complex navigation hierarchies
- Add route guards for role-based access control
- Implement breadcrumb navigation for better UX

**Modern Routing Implementation:**
- Route-based code splitting for performance
- Nested route patterns for complex applications
- Protected routes with role-based access control
- Dynamic route generation based on user permissions

**Navigation Flow Optimization:**
- {len(complex_flows)} high-complexity flows require careful redesign
- Average flow complexity: {avg_complexity:.1f}

"""

        content += """
### 3.2 State Management Migration

**From GWT Event Bus to Modern State Management:**

**State Management Strategy:**
- **Local State**: React useState and useReducer for component-specific state
- **Global State**: Redux Toolkit for cross-component state management
- **Server State**: React Query for API data management and caching
- **Form State**: React Hook Form for complex form handling

**Redux Store Structure:**
```typescript
// Store configuration
export const store = configureStore({{
    reducer: {{
        auth: authSlice.reducer,
        customer: customerSlice.reducer,
        products: productsSlice.reducer,
        billing: billingSlice.reducer,
        ui: uiSlice.reducer
    }},
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(apiSlice.middleware)
}});

// Typed hooks
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

## 4. MIGRATION TIMELINE AND PHASES

### 4.1 Phased Migration Approach

**Phase 1: Foundation Setup (4-6 weeks)**
- Development environment setup with modern toolchain
- Design system implementation with Material-UI
- Core component library development
- Testing infrastructure setup

**Phase 2: Core Components Migration (8-12 weeks)**
- High-priority component migration ({modernization_analysis.get('high_priority_count', 0)} components)
- Navigation and routing implementation  
- State management setup
- API integration layer

**Phase 3: Feature Migration (12-16 weeks)**
- Business domain component migration
- Complex workflow implementation
- Progressive Web App features
- Performance optimization

**Phase 4: Testing and Deployment (4-6 weeks)**
- Comprehensive testing and bug fixes
- User acceptance testing
- Production deployment
- Performance monitoring setup

### 4.2 Success Metrics and Quality Gates

**Performance Targets:**
- 50% improvement in load times
- 100% WCAG 2.1 AA compliance
- 90% user satisfaction rating
- 40% faster feature development
- 60% reduction in UI-related bugs

**Quality Assurance:**
- Automated testing coverage at 90%+
- Cross-browser compatibility validation
- Performance benchmarking
- Security compliance verification
- Accessibility audit completion

"""
        
        return content
    
    def generate_design_system_requirements(self, ui_analysis: Dict[str, Any]) -> str:
        """Generate design system requirements based on UI analysis"""
        ui_arch = ui_analysis.get('ui_architecture', {})
        timestamp = datetime.now().isoformat()
        
        content = f"""# Modern Design System Requirements

**Generated**: {timestamp}
**Category**: Design_System
**Mode**: enhanced_ui_analysis

## 1. DESIGN SYSTEM FOUNDATION

### 1.1 Design Token Architecture

**Token Categories:**
Based on the analysis of {len(ui_analysis.get('ui_components', {}))} UI components, the following design token system is required:

**Color Tokens:**
```json
{{
    "color": {{
        "brand": {{
            "primary": {{ "value": "#1976d2" }},
            "secondary": {{ "value": "#dc004e" }},
            "success": {{ "value": "#2e7d32" }},
            "warning": {{ "value": "#ed6c02" }},
            "error": {{ "value": "#d32f2f" }}
        }},
        "neutral": {{
            "50": {{ "value": "#fafafa" }},
            "100": {{ "value": "#f5f5f5" }},
            "200": {{ "value": "#eeeeee" }},
            "900": {{ "value": "#212121" }}
        }},
        "semantic": {{
            "text": {{
                "primary": {{ "value": "#212121" }},
                "secondary": {{ "value": "rgba(33, 33, 33, 0.6)" }}
            }},
            "background": {{
                "default": {{ "value": "#fafafa" }},
                "paper": {{ "value": "#ffffff" }}
            }}
        }}
    }}
}}
```

**Typography Tokens:**
```json
{{
    "typography": {{
        "fontFamily": {{
            "base": {{ "value": "'Roboto', 'Helvetica', 'Arial', sans-serif" }},
            "monospace": {{ "value": "'Roboto Mono', monospace" }}
        }},
        "fontSize": {{
            "xs": {{ "value": "0.75rem" }},
            "sm": {{ "value": "0.875rem" }},
            "base": {{ "value": "1rem" }},
            "lg": {{ "value": "1.125rem" }},
            "xl": {{ "value": "1.25rem" }},
            "2xl": {{ "value": "1.5rem" }}
        }},
        "lineHeight": {{
            "tight": {{ "value": "1.25" }},
            "normal": {{ "value": "1.5" }},
            "relaxed": {{ "value": "1.75" }}
        }}
    }}
}}
```

**Spacing Tokens:**
```json
{{
    "spacing": {{
        "0": {{ "value": "0" }},
        "1": {{ "value": "0.25rem" }},
        "2": {{ "value": "0.5rem" }},
        "3": {{ "value": "0.75rem" }},
        "4": {{ "value": "1rem" }},
        "6": {{ "value": "1.5rem" }},
        "8": {{ "value": "2rem" }},
        "12": {{ "value": "3rem" }},
        "16": {{ "value": "4rem" }}
    }}
}}
```

### 1.2 Component Design Principles

**Design System Principles:**
1. **Consistency**: All components follow the same visual language
2. **Accessibility**: WCAG 2.1 AA compliance built into every component
3. **Flexibility**: Components adapt to different use cases and contexts
4. **Performance**: Optimized for fast rendering and minimal bundle size
5. **Developer Experience**: Clear APIs and comprehensive documentation

**Component Architecture:**
- **Atomic Design**: Atoms, molecules, organisms, templates, pages
- **Composition Pattern**: Flexible component composition over inheritance
- **Prop-based Configuration**: Declarative component configuration
- **Theme Integration**: Consistent theming across all components

## 2. COMPONENT LIBRARY SPECIFICATION

### 2.1 Foundation Components (Atoms)

**Button Component:**
```typescript
interface ButtonProps {{
    variant?: 'contained' | 'outlined' | 'text';
    color?: 'primary' | 'secondary' | 'success' | 'error' | 'warning';
    size?: 'small' | 'medium' | 'large';
    disabled?: boolean;
    startIcon?: ReactNode;
    endIcon?: ReactNode;
    onClick?: (event: MouseEvent<HTMLButtonElement>) => void;
    children: ReactNode;
}}
```

**Input Components:**
- TextField (text, email, password, search types)
- Select (single and multi-select)
- Checkbox and Radio
- Switch and Toggle
- DatePicker and TimePicker
- Autocomplete with async loading

### 2.2 Layout Components (Molecules)

**Card Component:**
```typescript
interface CardProps {{
    elevation?: number;
    variant?: 'elevation' | 'outlined';
    children: ReactNode;
    actions?: ReactNode;
    header?: {{
        title: string;
        subtitle?: string;
        avatar?: ReactNode;
        action?: ReactNode;
    }};
}}
```

**DataTable Component:**
```typescript
interface DataTableProps<T> {{
    data: T[];
    columns: DataTableColumn<T>[];
    loading?: boolean;
    pagination?: PaginationProps;
    selection?: SelectionProps<T>;
    sorting?: SortingProps<T>;
}}
```

### 2.3 Complex Components (Organisms)

**Dashboard Widget:**
Based on the identified {ui_arch.get('total_components', 0)} UI components, standardized dashboard widgets are required:

```typescript
interface DashboardWidgetProps {{
    title: string;
    subtitle?: string;
    icon?: ReactNode;
    actions?: ReactNode;
    loading?: boolean;
    error?: string;
    children: ReactNode;
    size?: 'small' | 'medium' | 'large';
    responsive?: boolean;
}}
```

**Navigation Components:**
```typescript
interface NavigationProps {{
    items: NavigationItem[];
    currentPath: string;
    onNavigate: (path: string) => void;
    collapsed?: boolean;
    userMenu?: UserMenuProps;
}}
```

## 3. ACCESSIBILITY DESIGN STANDARDS

### 3.1 Accessibility Requirements

**WCAG 2.1 AA Compliance:**
- **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- **Keyboard Navigation**: All interactive elements keyboard accessible
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Focus Management**: Visible focus indicators and logical tab order
- **Animation Control**: Respect prefers-reduced-motion preference

**Implementation Standards:**
```typescript
// Accessible button with proper ARIA attributes
<Button
    aria-label="Save customer information"
    aria-describedby="save-button-description"
    disabled={{!isValid}}
>
    Save
</Button>
```

### 3.2 Inclusive Design Patterns

**User Preference Support:**
- High contrast mode compatibility
- Scalable typography (supports up to 200% zoom)
- Reduced motion animations
- Screen reader optimized content structure
- Keyboard-only navigation support

## 4. DOCUMENTATION AND TOOLING

### 4.1 Component Documentation

**Storybook Integration:**
- Interactive component playground
- Design token visualization  
- Accessibility testing integration
- Visual regression testing
- Code examples and usage guidelines

**Documentation Requirements:**
- Component API documentation
- Design guidelines and usage patterns
- Accessibility considerations
- Browser support matrix
- Performance characteristics

### 4.2 Development Tooling

**Design System Toolchain:**
- **Design Tokens**: Style Dictionary for token management
- **Component Library**: Rollup for optimized builds
- **Documentation**: Storybook with MDX documentation
- **Testing**: Jest + React Testing Library + jest-axe
- **Visual Testing**: Chromatic for visual regression testing
- **Linting**: ESLint + Prettier + Stylelint for code quality

**Quality Assurance:**
- Automated accessibility testing in CI/CD
- Performance budgets for component bundles  
- Cross-browser compatibility testing
- Design token validation and synchronization
- Component usage analytics and optimization

"""
        
        return content
    
    def generate_progressive_web_app_requirements(self, ui_analysis: Dict[str, Any]) -> str:
        """Generate PWA requirements"""
        timestamp = datetime.now().isoformat()
        
        content = f"""# Progressive Web App (PWA) Requirements

**Generated**: {timestamp}
**Category**: Progressive_Web_App
**Mode**: enhanced_ui_analysis

## 1. PWA CORE FEATURES

### 1.1 Service Worker Implementation

**Caching Strategy:**
- **App Shell**: Cache application shell for instant loading
- **API Responses**: Cache frequently accessed data with TTL
- **Assets**: Cache static assets (CSS, JS, images) with versioning
- **Dynamic Content**: Implement cache-first or network-first strategies

**Service Worker Features:**
```javascript
// Service worker registration
if ('serviceWorker' in navigator) {{
    navigator.serviceWorker.register('/sw.js')
        .then(registration => {{
            console.log('SW registered');
            
            // Handle updates
            registration.addEventListener('updatefound', () => {{
                const newWorker = registration.installing;
                newWorker.addEventListener('statechange', () => {{
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {{
                        // Show update available notification
                        showUpdateAvailableNotification();
                    }}
                }});
            }});
        }});
}}

// Offline functionality
self.addEventListener('fetch', event => {{
    if (event.request.destination === 'document') {{
        event.respondWith(
            fetch(event.request)
                .catch(() => caches.match('/offline.html'))
        );
    }}
}});
```

### 1.2 Web App Manifest

**Manifest Configuration:**
```json
{{
    "name": "A1 Telekom Austria Customer Care",
    "short_name": "A1 CuCo",
    "description": "Customer care management system for A1 Telekom Austria",
    "start_url": "/dashboard",
    "display": "standalone",
    "theme_color": "#1976d2",
    "background_color": "#ffffff",
    "orientation": "portrait-primary",
    "icons": [
        {{
            "src": "/icons/icon-192x192.png",
            "sizes": "192x192",
            "type": "image/png"
        }},
        {{
            "src": "/icons/icon-512x512.png",
            "sizes": "512x512",
            "type": "image/png"
        }},
        {{
            "src": "/icons/icon-maskable-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable"
        }}
    ]
}}
```

## 2. OFFLINE FUNCTIONALITY

### 2.1 Offline Data Management

**Offline Storage Strategy:**
- **IndexedDB**: Store critical business data for offline access
- **Cache API**: Store UI resources and API responses
- **Background Sync**: Queue actions for execution when online
- **Conflict Resolution**: Handle data conflicts when reconnecting

**Implementation:**
```typescript
// Offline data manager
class OfflineDataManager {{
    private db: IDBDatabase;
    
    async storeCustomerData(customers: Customer[]) {{
        const transaction = this.db.transaction(['customers'], 'readwrite');
        const store = transaction.objectStore('customers');
        
        for (const customer of customers) {{
            await store.put(customer);
        }}
    }}
    
    async getOfflineCustomers(): Promise<Customer[]> {{
        return new Promise((resolve, reject) => {{
            const transaction = this.db.transaction(['customers'], 'readonly');
            const store = transaction.objectStore('customers');
            const request = store.getAll();
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        }});
    }}
}}
```

## 3. PERFORMANCE OPTIMIZATION

### 3.1 Loading Performance

**Performance Metrics:**
- **First Contentful Paint**: < 1.5 seconds
- **Largest Contentful Paint**: < 2.5 seconds  
- **Time to Interactive**: < 3.8 seconds
- **Cumulative Layout Shift**: < 0.1

**Optimization Strategies:**
- **Code Splitting**: Route-based and component-based splitting
- **Lazy Loading**: Defer non-critical resources
- **Preloading**: Preload critical resources and routes
- **Image Optimization**: WebP format with lazy loading
- **Bundle Optimization**: Tree shaking and compression

### 3.2 Runtime Performance

**Memory Management:**
```typescript
// Efficient data management
const useVirtualizedList = <T>(items: T[], itemHeight: number) => {{
    const [visibleRange, setVisibleRange] = useState({{ start: 0, end: 10 }});
    
    const updateVisibleRange = useCallback((scrollTop: number, containerHeight: number) => {{
        const start = Math.floor(scrollTop / itemHeight);
        const end = Math.min(
            start + Math.ceil(containerHeight / itemHeight) + 1,
            items.length
        );
        
        setVisibleRange({{ start, end }});
    }}, [itemHeight, items.length]);
    
    return {{
        visibleItems: items.slice(visibleRange.start, visibleRange.end),
        visibleRange,
        updateVisibleRange
    }};
}};
```

## 4. SECURITY AND PRIVACY

### 4.1 PWA Security Standards

**Security Measures:**
- **HTTPS Only**: Enforce HTTPS for all PWA functionality
- **CSP Headers**: Content Security Policy for XSS protection
- **SRI**: Subresource Integrity for external resources
- **Permissions**: Request minimal necessary permissions
- **Data Encryption**: Encrypt sensitive data in local storage

### 4.2 Privacy Compliance

**Privacy Requirements:**
- **GDPR Compliance**: Data protection and user consent
- **Data Minimization**: Store only necessary data offline
- **User Control**: Clear data management options
- **Audit Trail**: Log data access and modifications
- **Secure Transmission**: End-to-end encryption for sensitive data

"""
        
        return content
    
    def _get_suggested_mui_components(self, component) -> str:
        """Get suggested Material-UI components for a GWT component"""
        suggestions = []
        
        for widget in component.gwt_widgets:
            if 'Tree' in widget:
                suggestions.append('TreeView')
            elif 'Grid' in widget or 'Table' in widget:
                suggestions.append('DataGrid')
            elif 'Panel' in widget:
                suggestions.append('Paper/Container')
            elif 'Button' in widget:
                suggestions.append('Button')
            elif 'Text' in widget:
                suggestions.append('TextField')
            elif 'List' in widget:
                suggestions.append('List/Select')
        
        return ', '.join(set(suggestions)) if suggestions else 'Card/Paper components'
    
    def _estimate_migration_time(self, component) -> str:
        """Estimate migration time for a component"""
        base_days = 3
        
        # Complexity factor
        complexity_factor = component.ui_complexity_score / 100
        base_days += complexity_factor * 5
        
        # Event handlers factor
        base_days += len(component.event_handlers) * 0.5
        
        # Business domain factor (more domains = more testing)
        base_days += len(component.business_domains) * 0.5
        
        return f"{int(base_days)}-{int(base_days * 1.5)}"
    
    def save_ui_modernization_requirements(self, ui_analysis: Dict[str, Any], mode: str) -> Dict[str, str]:
        """Generate and save all UI modernization requirements documents"""
        
        generated_files = {}
        
        try:
            # Generate component migration mapping
            migration_mapping = self.generate_component_migration_mapping(ui_analysis)
            migration_file = self.ui_modern_dir / "migration_strategy" / f"component_migration_mapping_{mode}.md"
            with open(migration_file, 'w', encoding='utf-8') as f:
                f.write(migration_mapping)
            generated_files['migration_mapping'] = str(migration_file)
            
            # Generate design system requirements
            design_system_req = self.generate_design_system_requirements(ui_analysis)
            design_file = self.ui_modern_dir / "design_system" / f"design_system_requirements_{mode}.md"
            with open(design_file, 'w', encoding='utf-8') as f:
                f.write(design_system_req)
            generated_files['design_system'] = str(design_file)
            
            # Generate PWA requirements
            pwa_req = self.generate_progressive_web_app_requirements(ui_analysis)
            pwa_file = self.ui_modern_dir / "progressive_web_app" / f"pwa_requirements_{mode}.md"
            with open(pwa_file, 'w', encoding='utf-8') as f:
                f.write(pwa_req)
            generated_files['pwa'] = str(pwa_file)
            
            logger.info(f"Generated {len(generated_files)} UI modernization documents")
            return generated_files
            
        except Exception as e:
            logger.error(f"Error generating UI modernization requirements: {e}")
            raise